from flask import Blueprint
from flask import render_template
from flask import request, jsonify
from flask_api import status
from TodoHandler import TodoHandler
import ResponseHandler
import DecodeToken
import re
import logging

todos = Blueprint('todos', __name__, template_folder='templates')

todo_handler = TodoHandler()

@todos.route('/', methods=['GET','POST'])
def new_todo():
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if response.method == 'POST':
            response_http_code = todo_handler.create(user_id, post_content.get("data"))
        elif response.method == 'GET':
            task_list = todo_handler.get_all_tasks(user_id)
            return jsonify(ResponseHandler.construct_json_response(
                {
                    "http_code": response_http_code,
                    "data": task_list
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

@todos.route('<todo_id>/', methods=['PUT', 'DELETE'])
def edit_todo(todo_id):
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'PUT':
            response_http_code = todo_handler.edit(user_id, todo_id, post_content.get("data"))
        elif request.method == 'DELETE':
            response_http_code = todo_handler.delete(user_id, todo_id)
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))

