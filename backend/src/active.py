from flask import Blueprint, request, jsonify

active = Blueprint('active',__name__,url_prefix="/active")

@active.post('/')
def upload_file():

    is_active = request.get_json()

    print(is_active)
    
    return jsonify({"POST":"test"})
    