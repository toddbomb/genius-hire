from flask import Blueprint, request
from src.database.chatHistory import memory
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
        model_response = rfi_response(query)
    
    
    return model_response
    
    

