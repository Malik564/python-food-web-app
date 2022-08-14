from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from flask_login import LoginManager


DB_NAME = 'databse'
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'Secrete'
    app.config["SQLALCHEMY_DATABASE_URI"]=f'sqlite:///{DB_NAME}.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    bcrypt.init_app(app)

    from .model import User , Restaurant, Items
    create_database(app)


    from .views import views
    app.register_blueprint(views , url_prefix = '/')

    from foodwebsite.auth.routes import auth
    app.register_blueprint(auth , url_prefix= '/')
    
    from foodwebsite.user.routes import users
    app.register_blueprint(users , url_prefix= '/')
    
    from foodwebsite.restaurants.routes import restaurants
    app.register_blueprint(restaurants , url_prefix= '/')

    from foodwebsite.cart.routes import cart
    app.register_blueprint(cart , url_prefix= '/')

    from foodwebsite.orders.routes import orders
    app.register_blueprint(orders , url_prefix= '/')

    login_manager.init_app(app)


    return app



def create_database(app):
    if not path.exists('foodwebsite/'+DB_NAME ):
        db.create_all(app = app)
        print('Databse created')

