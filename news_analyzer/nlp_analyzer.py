from flask import (Blueprint, Flask, flash, render_template, request,jsonify)
from google.cloud import language_v1
from news_analyzer.db import get_db
import os
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-mountain-308101-7fe5259b2655.json'

bp = Blueprint('nlp_analyzer', __name__, 
                url_prefix='/nlp_analyzer',
                static_folder='static',
                template_folder='templates')

@bp.route("/")
def index():
    db = get_db()
    files = db.execute('SELECT file_name,title,sentiment,sentiment_score,sentiment_magnitude FROM Files').fetchall()
    
    result = 'File_Name/title    Sentiment    sentiment_score    sentiment_magnitude\n'
    for f in files:
        if f[0]:
            f_line = f[0]+'    '+f[2]+'    '+'%.5f'%f[3]+'    '+'%.5f'%f[4]+'\n'
        else:
            f_line = f[1]+'    '+f[2]+'    '+'%.5f'%f[3]+'    '+'%.5f'%f[4]+'\n'
        result += f_line
    #print(result)
    return render_template("nlp_analyzer.html",result = result,title='NLP')

@bp.route("/", methods=["POST"])
def nlp():
    text = request.form.get('text')
    #nlp = get_nlp_attr(text)
    #print(nlp)
    return render_template("nlp_analyzer.html",title='NLP')