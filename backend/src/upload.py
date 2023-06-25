from flask import Blueprint, request, jsonify
from .util.Embed import call_embeddings
import pinecone
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone


upload = Blueprint('upload',__name__,url_prefix="/upload")

@upload.post('/')
def upload_file():
    file_object = request.files.get('file')

    loader = PyMuPDFLoader(file_object)
    pages = loader.load()

    embeddings = OpenAIEmbeddings()

    # initialize pinecone
    pinecone.init(
        api_key="035dee03-042d-4a6e-bc1b-a9a4a3546f2b",  # find at app.pinecone.io
        environment="northamerica-northeast1-gcp",  # next to api key in console
    )
    index_name = "langchain1"

    vectorstore = Pinecone.from_documents(pages, embeddings, index_name=index_name, namespace=file_object.filename)

    # call_embeddings(file) ??????
    print(file_object)
    # print(file_object.file)
    #call_embeddings(file_object)
    
    return jsonify({"POST":"test"})
    
    
    

