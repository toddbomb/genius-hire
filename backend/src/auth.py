from flask import Blueprint, request
from src.route import pick_tool
from src.database.chatHistory import memory
from src.util.query_data import get_pdf_qa_chain_response

auth = Blueprint('auth',__name__,url_prefix="/chat")

@auth.post('/')
def chat():
    request_data = request.get_json()

    try:
        query = request_data[0][0]['content']
    except:
        query = request_data['buttonText']

    model_response = get_pdf_qa_chain_response(query=query)
    
    return model_response
    
    

