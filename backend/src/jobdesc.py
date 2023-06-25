from flask import Blueprint, request, jsonify

jobdesc = Blueprint('jobdesc',__name__,url_prefix="/text")

@jobdesc.post('/')
def upload_file():

    job_description = request.get_json()

    print(job_description)
    
    return jsonify({"POST":"test"})
    
    
    

