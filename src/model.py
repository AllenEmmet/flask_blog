"""This file contains the User and Post classes"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """This class defines the users"""
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(120), unique=True)

    def __repr__(self):
        """Returns string representation of User"""
        return '<User %r>' % self.username

    def set_email(self, email):
        """Sets email"""
        self.email = email

    def set_password(self, password):
        """Sets password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Returns user id"""
        return self.id

    def set_admin(self):
        """Sets admin to True"""
        self.admin = True

    def is_admin(self):
        """Checks if admin is True"""
        return self.admin

class Post(db.Model):
    """This class defines the posts"""
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Returns string representation of Post"""
        return '<Post %r>' % self.title

    def set_title(self, title):
        """Sets title"""
        self.title = title

    def set_content(self, content):
        """Sets content"""
        self.content = content

    def set_date_posted(self, date_posted):
        """Sets date_posted"""
        self.date_posted = date_posted

    def set_user_id(self, user_id):
        """Sets foreign key"""
        self.user_id = user_id
