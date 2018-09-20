from flask import Blueprint
from flask import render_template
from flask import request, jsonify
from TaskHandler import TaskHandler
from TodoHandler import TodoHandler
import ResponseHandler
import DecodeToken
import re
import logging

tasks = Blueprint('tasks', __name__, template_folder='templates')

task_handler = TaskHandler()
todo_handler = TodoHandler()

@tasks.route('/', methods=['POST'])
def new_task():
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        response_http_code = task_handler.create(user_id, post_content.get("data"))
    else:
        response_http_code = 403

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))

@tasks.route('<task_id>/', methods=['PUT', 'DELETE'])
def edit_or_delete_task(task_id):
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'PUT':
            response_http_code = task_handler.edit(user_id, task_id, post_content.get("data"))
        elif request.method == 'DELETE':
            response_http_code = task_handler.delete(user_id, task_id)
    else:
        response_http_code = 403

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))

@tasks.route('/<task_id>/todos/', methods=['POST'])
def new_todo(task_id):
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        response_http_code = todo_handler.create(user_id, task_id, post_content.get("data"))
    else:
        response_http_code = 403

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))

@tasks.route('<task_id>/todos/<todo_id>/', methods=['PUT', 'DELETE'])
def edit_or_delete_todo(task_id, todo_id):
    post_content = request.json
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'PUT':
            response_http_code = todo_handler.edit({
                "user_id": user_id,
                "task_id": task_id,
                "todo_id": todo_id
            }, post_content.get("data"))
        elif request.method == 'DELETE':
            response_http_code = todo_handler.delete({
                "user_id": user_id,
                "task_id": task_id,
                "todo_id": todo_id
            })
    else:
        response_http_code = 403

    return jsonify(ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    ))
