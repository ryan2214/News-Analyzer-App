from flask import (Blueprint, Flask, render_template, request)
from google.cloud import language_v1
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-mountain-308101-7fe5259b2655.json'

bp = Blueprint('nlp_analyzer', __name__, url_prefix='/nlp_analyzer')

@bp.route("/")
def index():
    return "NLP Analyzer"

@bp.route("/nlp/<text_content>", methods=["GET"])
def analyze_nlp(text_content):

    client = language_v1.LanguageServiceClient()
    
    type_ = language_v1.Document.Type.PLAIN_TEXT
    
    language = "en"
    
    document = {"content": text_content, "type_": type_, "language": language}
    
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    nlp = {
        "sentiment_score": "",
        "sentiment_magnitude": "",
        "sentiment": ""
        }

    nlp["sentiment_score"] = response.document_sentiment.score
    nlp["sentiment_magnitude"] = response.document_sentiment.magnitude
    
    if response.document_sentiment.score < 0:
        nlp["sentiment"] = "negative"
    elif response.document_sentiment.score > 0:
        nlp["sentiment"] = "positive"
    else:
        nlp["neutral"] = "neutral"

    return jsonify(nlp)