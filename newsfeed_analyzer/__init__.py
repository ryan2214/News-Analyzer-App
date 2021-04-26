import os
from flask import Flask

UPLOAD_FOLDER = '/home/ubuntu'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
basedir = os.path.abspath(os.path.dirname(__file__))

from .db import close_connection
app.teardown_appcontext(close_connection)

import newsfeed_analyzer.views

import newsfeed_analyzer.auth
app.register_blueprint(auth.bp)

import newsfeed_analyzer.file_uploader
app.register_blueprint(file_uploader.bp)

import newsfeed_analyzer.newsfeed_ingester
app.register_blueprint(newsfeed_ingester.bp)

import newsfeed_analyzer.nlp_analyzer
app.register_blueprint(nlp_analyzer.bp)



