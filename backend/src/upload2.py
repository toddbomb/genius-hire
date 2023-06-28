from flask import Blueprint, request, jsonify
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from src.database.TemplateInfo import JD
import fitz

upload = Blueprint('upload',__name__,url_prefix="/upload2")

@upload.post('/')
def upload_file():
    global file_name
    
    file_object = request.files.get('file')
    file_name = file_object.filename

    
    return jsonify({"POST":"test"})
    
    
    