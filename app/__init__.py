# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, request
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_babel import lazy_gettext as _l

from config import Config

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
mail = Mail(application)
bootstrap = Bootstrap(application)
moment = Moment(application)
babel = Babel(application)


from app import errors, models, routes

if not application.debug:
    if application.config['MAIL_SERVER']:
        auth = None
        if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
            auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
        secure = None
        if application.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
            fromaddr='no-reply@' + application.config['MAIL_SERVER'],
            toaddrs=application.config['ADMINS'], subject='Checkiner Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.WARNING)
        application.logger.addHandler(mail_handler)

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/checkiner.log', maxBytes=10240,
                                   backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.WARNING)
application.logger.addHandler(file_handler)
application.logger.setLevel(logging.WARNING)
application.logger.info('Checkiner startup')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(application.config['LANGUAGES'])
