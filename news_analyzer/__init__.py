import os
from flask import Flask
basepath = os.path.dirname(__file__)
CURRENT_FOLDER = basepath

app = Flask(__name__)
app.secret_key = "secret key"
app.config['CURRENT_FOLDER'] = CURRENT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
basedir = os.path.abspath(os.path.dirname(__file__))

from .db import close_connection
app.teardown_appcontext(close_connection)

import news_analyzer.views

import news_analyzer.auth
app.register_blueprint(auth.bp)

import news_analyzer.file_uploader
app.register_blueprint(file_uploader.bp)

import news_analyzer.file_management
app.register_blueprint(file_management.bp)

import news_analyzer.news_ingester
app.register_blueprint(news_ingester.bp)

import news_analyzer.nlp_analyzer
app.register_blueprint(nlp_analyzer.bp)



