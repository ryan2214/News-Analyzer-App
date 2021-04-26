# -*- coding:utf-8 -*-
import os
from pathlib import Path
from flask import jsonify
# Imports the Google Cloud client library
from google.cloud import language_v1

def get_nlp_score(text):
    # Instantiates a NLP client
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    SENTI_RESULT = client.analyze_sentiment(request={'document': document}).document_sentiment.score

    return SENTI_RESULT

def get_nlp_attr(text_content): 

    client = language_v1.LanguageServiceClient()
    
    type_ = language_v1.Document.Type.PLAIN_TEXT
    
    language = "en"
    
    document = {"content": text_content, "type_": type_, "language": language}
    
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type}).document_sentiment
    #print("Sentiment: {}, {}".format(response.score, response.magnitude))
    nlp = {
        "sentiment_score": "",
        "sentiment_magnitude": "",
        "sentiment": ""
        }
    
    nlp["sentiment_score"] = response.score
    nlp["sentiment_magnitude"] = response.magnitude
    
    if response.score < 0:
        nlp["sentiment"] = "negative"
    elif response.score > 0:
        nlp["sentiment"] = "positive"
    else:
        nlp["sentiment"] = "neutral"

    return nlp