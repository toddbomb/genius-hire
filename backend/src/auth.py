from flask import Blueprint, request
from src.database.chatHistory import memory
from src.util.query_data import get_pdf_qa_chain_response
from src.util.rfi_builder import rfi_response
from src.util.demodetails import details
from src.database.TemplateInfo import JD



auth = Blueprint('auth',__name__,url_prefix="/chat")

@auth.post('/')
def chat():
    request_data = request.get_json()

    print(request_data)

    try:
        query = request_data[0][0]['content']
    except:
        try:
            query = request_data['prompt_template']
        except KeyError:
            query = None

    # Performance data
    model_response = details(query)

    # RFI
    if model_response == '':
        model_response = get_pdf_qa_chain_response(query=query,job_description=JD[0], filename=JD[1])
    
    
    return model_response
    
    

