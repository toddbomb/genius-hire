from flask import Blueprint, request, jsonify
from src.database.JobDescription import job_description, job_title

jobdesc = Blueprint('jobdesc',__name__,url_prefix="/text")

@jobdesc.post('/')
def upload_file():

    job_json = request.get_json()

    # with open("/backend/src/database/jobdescription.txt", "w") as f:
    #     f.write(job_json['title'])
    #     f.write(job_json['text'])

    print(job_json)

    return jsonify({"POST":"test"})
    
    
    

