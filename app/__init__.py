from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail, Message
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown


bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
login_manager.session_protection = 'strong' # flask-login will keep track of ip and broswer agent, will log user out if it detects a change
login_manager.login_view = 'auth.login'


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)

	from .main import main as main_blueprint
	from .auth import auth as auth_blueprint
	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix='/auth')


	return app



