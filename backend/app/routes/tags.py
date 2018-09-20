from flask import Blueprint
from flask import render_template
from flask import request, jsonify
from flask_api import status
from TagsHandler import TagsHandler
import ResponseHandler
import DecodeToken

tags = Blueprint('tags', __name__, template_folder='templates')

tags_handler = TagsHandler()

@tags.route('/', methods=['GET','POST'])
def new_tags():
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'POST':
            post_content = request.json
            response_http_code = tags_handler.create(user_id, post_content.get("data"))
        elif request.method == 'GET':
            response = tags_handler.get_tags()
            return jsonify(ResponseHandler.construct_json_response(
                {
                    "http_code": response.get("http_code"),
                    "data": response.get("data")
                }
            ))
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))

@tags.route('/top/<number>/', methods=['GET'])
def top_tags_of_user(number):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        response = tags_handler.get_top_tags(user_id, number)
        return jsonify(ResponseHandler.construct_json_response(
            {
                "http_code": response.get("http_code"),
                "data": response.get("data")
            }
        ))
    else:
        response_http_code = status.HTTP_403_FORBIDDEN
        return jsonify(ResponseHandler.construct_json_response(
            {
                "http_code": response_http_code,
                "http_code_only": True
            }
        ))
