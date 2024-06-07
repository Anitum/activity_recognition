from flask import render_template, flash , redirect
from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user , login_user, logout_user

@app.route('/')
@app.route('/index')

def index():
	user = {'username': 'Miguel'}
	posts = [
				{
				'author': {'username': 'John'},
				'body': 'Beautiful day in Portland!'
				},
				{
				'author': {'username': 'Susan'},
				'body': 'The Avengers movie was so cool!'
				}
			]
	return render_template('index.html', title='Home', user=user, posts=posts)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
    	
# 		return redirect('/index')
    
# 	return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated():
		return redirect('/index')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None: 
			return flash('Invalid Username')
		
		if not user.check_password(form.password.data):
			return flash('Invalid Password')

		login_user(user , remember=form.remember_me.data)
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')