from flask import Blueprint, request
from src.route import pick_tool
from src.database.chatHistory import memory
from src.util.query_data import get_pdf_qa_chain_response
from src.database.JobDescription import job_description, job_title
from src.database.FileName import file_name

auth = Blueprint('auth',__name__,url_prefix="/chat")

@auth.post('/')
def chat():
    request_data = request.get_json()

    try:
        query = request_data[0][0]['content']
    except:
        query = request_data['buttonText']

    with open("backend/src/database/filename.txt", "r") as f:
        file_name = f.read()
    
    with open("backend/src/database/jobdescription.txt", "r") as f:
        job_description = f.read()
        
    print(job_description, file_name)
    model_response = get_pdf_qa_chain_response(query=query, filename='exresumes.pdf', job_description=job_description)
    
    return model_response
    
    

