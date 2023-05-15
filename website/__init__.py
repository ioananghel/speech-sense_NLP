from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # initialises the package   
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET Key For App Encryption (cookies and session data)'
    # this stores the database in the website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # fstring -> it allows vars
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # all urls start with /
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    # helps manage login related things
    login_manager = LoginManager()
    # if not logged in and login required -> auth.login
    login_manager.login_view = 'auth.login'
    # tells the manager which app we're using
    login_manager.init_app(app)
    
    ROOT_DIR = path.dirname(path.abspath("__init__.py"))

    print(ROOT_DIR)
    # tells flask what user to load
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
