from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin
from app import db, lm


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	social_id = db.Column(db.String(64), nullable=False)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id) # python 2
		except NameError:
			return str(self.id) #python 3

	def __repr__(self):
		return '<User {0}>'.format(self.nickname)

@lm.user_loader
def load_user(id):
	return User.query.get(id)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
			return '<Post {0}>'.format(self.body)