#!usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, flash, render_template, url_for, session, redirect
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager, Shell
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from datetime import datetime
import config import config
from threading import Thread


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)

app.config.from_object(config['development'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

DEBUG = True


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username



class NameForm(Form):

    """docstring for NameForm"""

    name = StringField(u'请输入您的姓名：', validators=[Required()])
    submit = SubmitField(u'提交')


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('db', MigrateCommand)
# 在创建了新列或添加新表格等改动数据库结构时，才需要进行数据库迁移，即upgrade操作
# Flask Web Development书中关于迁移的部分，应在手动进行数据库操作前进行
manager.add_command('shell', Shell(make_context=make_shell_context))


# send asynchrous email
def send_async_mail(app, msg):
	with app.app_context():
		mail.send(msg)

def send_mail(to, subject, template, **kwargs):
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_mail, args=[app, msg])
	thr.start()
	return thr

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
    	user = User.query.filter_by(username=form.name.data).first()
    	if user is None:
    		user = User(username=form.name.data)
    		db.session.add(user)
    		db.session.commit()
    		session['known'] = False
    		if app.config['FLASKY_ADMIN']:
    			subject = 'A new user has just registered with your site.'
    			send_mail(app.config['FLASKY_ADMIN'], subject, 'mail/new_user', user=user)
    	else:
    		session['known'] = True
    	session['name'] =form.name.data
    	form.name.data = ''
    	return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow(), known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manager.run()
