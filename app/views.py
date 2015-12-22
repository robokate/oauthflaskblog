from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User
from oauth import OAuthSignIn


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	posts = user.posts
	return render_template('index.html',
							title='Home',
							user=user,
							posts=posts,
							links=get_nav_links())

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html', links=get_nav_links())


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()


@app.route('/callback/<provider>/')
def oauth_callback(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email = oauth.callback()
	if social_id is None:
		flash('Authentication failed.')
		return redirect(url_for('index'))
	user = User.query.filter_by(social_id=social_id).first()
	if not user:
		user = User(social_id=social_id, nickname=username, email=email)
		db.session.add(user)
		db.session.commit()
	login_user(user, True)
	return redirect(url_for('index'))


def get_nav_links():
	links = []
	links.append({'url': url_for('index'), 'title': 'Home'})
	if not current_user.is_anonymous:
		links.append({'url': url_for('logout'), 'title': 'Logout'})
	else:
		links.append({'url': url_for('login'), 'title': 'Login'})
	return links