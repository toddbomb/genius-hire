from flask import Blueprint, request, jsonify
from .util.Embed import call_embeddings

upload = Blueprint('upload',__name__,url_prefix="/upload")

@upload.post('/')
def upload_file():
    file_object = request.files.get('file')

    # call_embeddings(file) ??????
    print(file_object)
    print(file_object.file)
    #call_embeddings(file_object)
    
    return jsonify({"POST":"test"})
    
    
    

