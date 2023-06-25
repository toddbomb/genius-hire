from flask import Blueprint, request, jsonify
from src.database.chatHistory import memory
jobdesc = Blueprint('jobdesc',__name__,url_prefix="/text")

@jobdesc.post('/')
def upload_file():

    job_description = request.get_json()

    print(job_description)
    memory.chat_memory.add_user_message(job_description)
    
    return jsonify({"POST":"test"})
    
    
    

