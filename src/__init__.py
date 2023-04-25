from flask import Flask
from .model import db, User
from .views import views
from flask_login import LoginManager

def main():
    app = Flask(__name__)
    SECRET_KEY = '1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    db.app=app

    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    app.register_blueprint(views)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app