from flask import (Blueprint, Flask, flash, request, redirect, render_template, json, jsonify, url_for)
from werkzeug.utils import secure_filename
from .senti_analyze import *
from PyPDF2 import PdfFileReader
import cv2
from datetime import date,datetime
from news_analyzer import app
from news_analyzer.db import get_db
import os

from news_analyzer import senti_analyze

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-mountain-308101-7fe5259b2655.json'

bp = Blueprint('file_uploader', __name__, 
                url_prefix='/file_uploader',
                static_folder='static',
                template_folder='templates')

ALLOWED_PICTURE_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
ALLOWED_TEXT_EXTENSIONS = set(['pdf', 'txt'])
 
def is_picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_PICTURE_EXTENSIONS

def is_text(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_TEXT_EXTENSIONS

	
@bp.route('/')
def index():
	return render_template('file_uploader.html',title='File Upload',year=datetime.now().year)

@bp.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and (is_picture(f.filename) or is_text(f.filename))):
            return jsonify({"error": 1001, "msg": "please check file type，limited to pdf, txt, png, PNG, jpg, JPG, bmp"})

        if (is_picture(f.filename)):
    
            basepath = os.path.dirname(__file__)  # current path
    
            upload_path = os.path.join(basepath, 'upload/images', secure_filename(f.filename))  # make sure path exists
            f.save(upload_path)
    
            # Opencv read picture
            img = cv2.imread(upload_path)
            cv2.imwrite(os.path.join(basepath, 'upload/images', 'output.jpg'), img)
    
            return render_template('upload_pic_ok.html')
        
        if (is_text(f.filename)):

            basepath = os.path.dirname(__file__)  # current path
            upload_path = os.path.join(basepath, 'upload/text', secure_filename(f.filename))  # make sure pwd exists
            f.save(upload_path)           

            if(f.filename.rsplit('.', 1)[1]=='pdf'): # process pdf
                create_file(upload_path)
                os.remove(upload_path)
            flash('File successfully uploaded')
            return redirect('/')
 
        else:
            flash('Allowed file types are txt, pdf')
            return redirect(request.url)
        
def extract_metadata(file):
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            #number_of_pages = pdf.getNumPages()
            
        metadata = {
            "title": "",
            "author": ""
        }
        metadata["title"] = info.title
        metadata["author"] = info.author
        return metadata 

def extract_text(file):
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            page = pdf.getPage(0)
            text = page.extractText()
            return text

def create_file(file):
        split_tup = os.path.splitext(file) 
        metadata = extract_metadata(file)  
        text_content = extract_text(file)
        nlp = senti_analyze.get_nlp_attr(text_content) 

        file_name = split_tup[0].rsplit('\\',1)[1]
        upload_date = str(date.today())
        text = text_content
        title = metadata["title"]
        author = metadata["author"]
        sentiment_score = nlp["sentiment_score"]
        sentiment_magnitude = nlp["sentiment_magnitude"]
        sentiment = nlp["sentiment"]
        db = get_db()
        if db.execute('SELECT file_name FROM Files WHERE file_name = ?', (file_name,)).fetchone() == None:
            db.execute(
                'INSERT INTO Files (file_name, upload_date, text, title, author, sentiment_score, sentiment_magnitude, sentiment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (file_name, upload_date, text, title, author, sentiment_score, sentiment_magnitude, sentiment,)
            )
            db.commit()
            app.logger.info('Successfully added to DB')
        app.logger.info('create_file completed')

     
def view_file():
    db = get_db()
    files = db.execute('SELECT * FROM Files').fetchall()
    return files