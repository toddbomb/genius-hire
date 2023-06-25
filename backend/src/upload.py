from flask import Blueprint, request, jsonify
from .util.Embed import call_embeddings
import pinecone
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import PyPDF2
import io


upload = Blueprint('upload',__name__,url_prefix="/upload")

@upload.post('/')
def upload_file():
    file_object = request.files.get('file')
    file_name = request.files.get('filename')

    print(request)
    print(file_object)

    pdf_stream = io.BytesIO(file_object.read())
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    # Loop through the pages and extract the text

    embeddings = OpenAIEmbeddings()

    pinecone.init(
        api_key="035dee03-042d-4a6e-bc1b-a9a4a3546f2b",  # find at app.pinecone.io
        environment="northamerica-northeast1-gcp",  # next to api key in console
    )
    index_name = "langchain1"

    pdf_texts = []

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        pdf_texts.append(text)

        print(text)

    vectorstore = Pinecone.from_texts(pdf_texts, embeddings, index_name=index_name, namespace=file_name)



    # initialize pinecone


    # call_embeddings(file) ??????
    print(file_object)
    # print(file_object.file)
    #call_embeddings(file_object)
    
    return jsonify({"POST":"test"})
    
    
    

