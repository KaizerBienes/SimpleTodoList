from flask import Blueprint, Response
from flask import request

accounts = Blueprint('accounts', __name__, template_folder='templates')

from Registration import Registration
from Authentication import Authentication
import ResponseHandler

registration = Registration()
authentication = Authentication()

@accounts.route('/register/', methods=['POST'])
def register():
    post_content = request.json
    http_code = registration.register_user(post_content) 
    return ResponseHandler.construct_json_response(
        {
            "http_code": http_code,
            "http_code_only": True,
        }
    )

@accounts.route('/login/', methods=['POST'])
def login():
    post_content = request.json
    response = authentication.login(post_content)
    return ResponseHandler.construct_json_response(
        {
            "http_code": response.get("http_code"),
            "data": response.get("data")
        }
    )
