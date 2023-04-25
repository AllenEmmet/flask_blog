"""This file contains all routes and Form classes for the site"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from .model import db, User, Post

views = Blueprint('views', __name__)

class LoginForm(FlaskForm):
    """Form for login page"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Form for registration page"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Password2', validators=[DataRequired(), Length(min=8)])
    admin = BooleanField('admin')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """Form for post publication page"""
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])

@views.route('/')
def base():
    """Redirects to home route"""
    return redirect(url_for('views.home'))

@views.route('/home')
def home():
    """Directs to home page"""
    users = User.query.all()
    posts = Post.query.all()
    return render_template('home.html', users=users, posts=posts, User=User, user=current_user)

@views.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in existing users"""
    form = LoginForm()
    if request.method == 'POST':

        # get the username and password from the form
        email = request.form['email']
        password = request.form['password']

        # get the user from the database
        user = User.query.filter_by(email=email).first()

        # check if the user exists and the password is correct
        if user and user.check_password(password):
            # log the user in
            login_user(user)
            if user.admin:
                return redirect(url_for('views.admin'))

            return redirect(url_for('views.base'))
        # tell the user the login failed
        return render_template('login.html', error='Invalid username or password', form=form)

    return render_template('login.html', form=form)

@views.route('/register', methods=['GET', 'POST'])
def register():
    """Creates and saves new users"""
    form=RegisterForm()

    if request.method == 'POST':
        # get the username and password from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # check if the username is already taken
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already taken', form=form)
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already in use', form=form)
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match', form=form)
        if len(password) < 8:
            return render_template('register.html', error='Password 8 char min', form=form)

        if form.validate_on_submit():
            # create a new user
            user = User(username=username)
            user.set_email(email)
            user.set_password(password)

            # check if the user is an admin
            if request.form.get('usertype') == 'admin':
                user.set_admin()

            # add the user to the database
            db.session.add(user)
            db.session.commit()

            # log the user in
            login_user(user)

            if user.admin:
                return redirect(url_for('views.admin'))
            return redirect(url_for('views.base'))


        return render_template('register.html', error='One or more field was invalid', form=form)

    return render_template('register.html', form=form)

@views.route('/logout')
@login_required
def logout():
    """Logs user out"""
    if current_user.is_authenticated:
        print('trig')
        logout_user()
    return redirect(url_for('views.base'))

@views.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    """Creates and saves new posts"""
    if request.method == 'POST':
        # get the post information from the form
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.id

        # check if the user is logged in
        if current_user.is_authenticated:
            post = Post()
            post.set_title(title)
            post.set_content(content)
            post.set_user_id(user_id)
            # add the post to the database
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('views.base'))
        return render_template(url_for('views.base'), error='Please log in to create a post')
    return render_template('post.html')

@views.route('/admin')
def admin():
    """Directs to admin page as appropriate"""
    if current_user.admin:
        users = User.query.all()
        return render_template('admin.html', users=users)

    return redirect(url_for('views.base'))

@views.route('/about')
def about():
    """Directs to about page"""
    return render_template('about.html')
