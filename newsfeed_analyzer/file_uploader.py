from flask import (Blueprint, Flask, flash, request, redirect, render_template, json, jsonify, url_for)
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader
from datetime import date
from newsfeed_analyzer import app
from newsfeed_analyzer.db import get_db
import os
import urllib.request
from google.cloud import language_v1
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-mountain-308101-7fe5259b2655.json'

bp = Blueprint('file_uploader', __name__, url_prefix='/file_uploader')

ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@bp.route('/')
def index():
	return render_template('upload.html')

@bp.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf')
			return redirect(request.url)
        
@bp.route('/file/metadata/<file>', methods=['GET'])
def extract_metadata(file):
    if file and allowed_file(file):
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            
        metadata = {
            "title": "",
            "author": ""
        }
        metadata["title"] = info.title
        metadata["author"] = info.author
        return metadata 
    else:
        return jsonify({"error": "There is no such file",}), 403

@bp.route('/file/text/<file>', methods=['GET'])
def extract_text(file):
    if file and allowed_file(file):
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            page = pdf.getPage(1)
            text = page.extractText()
            return text
    else:
        return jsonify({"error": "There is no such file",}), 403
 
def analyze_nlp(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    nlp = { "sentiment_score": "", "sentiment_magnitude": "", "sentiment": "" }
    nlp["sentiment_score"] = response.document_sentiment.score
    nlp["sentiment_magnitude"] = response.document_sentiment.magnitude
    
    if response.document_sentiment.score < 0:
        nlp["sentiment"] = "negative"
    elif response.document_sentiment.score > 0:
        nlp["sentiment"] = "positive"
    else:
        nlp["neutral"] = "neutral"
    return nlp

@bp.route('/file/create/<file>', methods=['GET'])
def create_file(file):
    if file and allowed_file(file):
        split_tup = os.path.splitext(file) 
        metadata = extract_metadata(file)  
        text_content = extract_text(file)
        nlp = analyze_nlp(text_content) 

        file_name = split_tup[0]
        upload_date = str(date.today())
        text = text_content
        title = metadata["title"]
        author = metadata["author"]
        sentiment_score = nlp["sentiment_score"]
        sentiment_magnitude = nlp["sentiment_magnitude"]
        sentiment = nlp["sentiment"]

        db = get_db()
        db.execute(
            'INSERT INTO Files (file_name, upload_date, text, title, author, sentiment_score, sentiment_magnitude, sentiment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (file_name, upload_date, text, title, author, sentiment_score, sentiment_magnitude, sentiment,)
        )
        db.commit()
        app.logger.info('Successfully added to DB')
        return 'Successfully added to DB', 200
    else:
        return jsonify({"error": "There is no such file",}), 403
        
@bp.route('/file/delete/<file_id>', methods=['GET', 'POST'])       
def delete_article(file_id):
    db = get_db()
    files = db.execute(
        'SELECT * FROM Files WHERE file_id = ?', (file_id,)
    ).fetchone()
    if files is None:
        return jsonify({"error": "There is no such file",}), 403
    else:
        db.execute('DELETE FROM Files WHERE file_id = ?', (file_id,))
        db.commit()
        app.logger.info('Successfully deleted the file')
        return 'Successfully deleted the file', 200

@bp.route('/file/view', methods=['GET'])       
def view_file():
    db = get_db()
    files = db.execute('SELECT * FROM Files').fetchall()
    return jsonify(files)