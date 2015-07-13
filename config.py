#!usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = 'veryhardpwwd' # needs to be set in a environment variable
	SQLAlCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SUBJECT_PREFIX = 'Learning Flask '
	MAIL_SENDER = 'Flasky Admin <sbjdmx@126.com>'
	FLASKY_ADMIN = 'songbingjin@126.com' # should be set in an environment variable
	# FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 10
	
	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	"""docstring for DevelopmentConfig"""
	DEBUG = True
	MAIL_SERVER = 'smtp.126.com'
	MAIL_PORT = 25
	MAIL_USERNAME = 'sbjdmx@126.com'
	MAIL_PASSWORD = 'wodedaxuemeng'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite' ) 
		

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')



config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
# DEBUG = True


# app.config['MAIL_SERVER'] = 'smtp.126.com'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USERNAME'] ='sbjdmx@126.com'
# app.config['MAIL_PASSWORD'] = 'wodedaxuemeng'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLAlCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['MAIL_SUBJECT_PREFIX'] = 'Learning Flask '
# app.config['MAIL_SENDER'] = 'Flasky Admin <sbjdmx@126.com>'
# app.config['FLASKY_ADMIN'] = 'songbingjin@126.com'