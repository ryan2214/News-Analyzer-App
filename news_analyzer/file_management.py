from flask import (Blueprint, Flask, flash, request, redirect, render_template, json, jsonify, url_for)
from werkzeug.utils import secure_filename
from datetime import datetime
from news_analyzer import app
from news_analyzer.db import get_db
import os


#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-mountain-308101-7fe5259b2655.json'

bp = Blueprint('file_management', __name__, 
                url_prefix='/file_management',
                static_folder='static',
                template_folder='templates')

def view_file():
    db = get_db()
    files = db.execute('SELECT * FROM Files').fetchall()
    result = ""
    for f in files:
        if f[0]:
            result += "File Name: "+f[0]+'\n'
        if f[3]:
            result += "Title: "+f[3]+'\n'
        if f[4]:
            result += "Author: "+f[4]+'\n'
        if f[1]:
            result += "Upload Date: "+f[1]+'\n'
        if f[2]:
            result += "Content: "+f[2]+'\n'     
        if f[8]:
            result += "Description: "+f[8]+'\n'
        if f[9]:
            result += "URL: "+f[9]+'\n'
        result += "Sentiment Score: "+str(f[5])+'\n'
        result += "Sentiment Magnitude: "+str(f[6])+'\n'
        result += "Sentiment: "+f[7]+'\n\n'
    return result

def open_file(file_name):
    db = get_db()
    file = db.execute(
        'SELECT * FROM Files WHERE file_name = ?', (file_name,)
    ).fetchone()
    if file is None:
        file = db.execute(
            'SELECT * FROM Files WHERE title = ?', (file_name,)
        ).fetchone()
        if file is None:
            app.logger.info('no file named this')
        else:
            #for f in file:
            result = ""
            if file[0]:
                result += "File Name: "+file[0]+'\n'
            if file[3]:
                result += "Title: "+file[3]+'\n'
            if file[4]:
                result += "Author: "+file[4]+'\n'
            if file[1]:
                result += "Upload Date: "+file[1]+'\n'
            if file[2]:
                result += "Content: "+file[2]+'\n'
            if file[8]:
                result += "Description: "+file[8]+'\n'
            if file[9]:
                result += "URL: "+file[9]+'\n' 
            result += "Sentiment Score: "+str(file[5])+'\n'
            result += "Sentiment Magnitude: "+str(file[6])+'\n'
            result += "Sentiment: "+file[7]+'\n\n'
            
            #print(result)
            app.logger.info('Successfully opened the file')
            return result

    else:
        #for f in file:
        result = ""
        if file[0]:
            result += "File Name: "+file[0]+'\n'
        if file[3]:
            result += "Title: "+file[3]+'\n'
        if file[4]:
            result += "Author: "+file[4]+'\n'
        if file[1]:
            result += "Upload Date: "+file[1]+'\n'
        if file[2]:
            result += "Content: "+file[2]+'\n'
        if file[8]:
            result += "Description: "+file[8]+'\n'
        if file[9]:
            result += "URL: "+file[9]+'\n' 
        result += "Sentiment Score: "+str(file[5])+'\n'
        result += "Sentiment Magnitude: "+str(file[6])+'\n'
        result += "Sentiment: "+file[7]+'\n\n'
          
        #print(result)
        app.logger.info('Successfully opened the file')
        return result
        

def delete_file(file_name):
    db = get_db()
    files = db.execute(
        'SELECT * FROM Files WHERE file_name = ?', (file_name,)
    ).fetchone()
    if files is None:
        files = db.execute(
            'SELECT * FROM Files WHERE title = ?', (file_name,)
        ).fetchone()
        if files is None:
            app.logger.info('no file named this')
        else:
            db.execute('DELETE FROM Files WHERE title = ?', (file_name,))
            db.commit()
            app.logger.info('Successfully deleted the news')
    else:
        db.execute('DELETE FROM Files WHERE file_name = ?', (file_name,))
        db.commit()
        app.logger.info('Successfully deleted the file')

@bp.route('/')
def index():
    files = view_file()
    return render_template('file_management.html',result = files,title='File Management',year=datetime.now().year)

@bp.route('/', methods=['POST'])
def management():
    if request.method == 'POST':
        f_name = request.form.get('file_name')
        op = request.form.get('op')
        if op == 'open':
            f = open_file(f_name)
            return render_template('file_management.html',result = f,title='File Management',year=datetime.now().year)
        elif op == 'delete':
            delete_file(f_name)
            files = view_file()
            return render_template('file_management.html',result = files,title='File Management',year=datetime.now().year)
        #elif op == 'query':
        return redirect('/')


     

