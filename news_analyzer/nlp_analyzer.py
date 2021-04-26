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
    files = db.execute('SELECT file_name,sentiment,sentiment_score,sentiment_magnitude FROM Files').fetchall()
    
    result = 'File_Name\tSentiment\tsentiment_score\tsentiment_magnitude\n'
    for f in files:
        f_line = f[0]+'\t'+f[1]+'\t'+str(f[2])+'\t'+str(f[3])+'\n'
        result += f_line
    #print(result)
    return render_template("nlp_analyzer.html",result = result,title='NLP')

@bp.route("/", methods=["POST"])
def nlp():
    text = request.form.get('text')
    #nlp = get_nlp_attr(text)
    #print(nlp)
    return render_template("nlp_analyzer.html",title='NLP')