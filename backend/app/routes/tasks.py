from flask import Blueprint
from flask import render_template
from flask import request
from TaskHandler import TaskHandler
from TodoHandler import TodoHandler
from TodoTagsHandler import TodoTagsHandler
import ResponseHandler
import DecodeToken
from flask_api import status

tasks = Blueprint('tasks', __name__, template_folder='templates')

task_handler = TaskHandler()
todo_handler = TodoHandler()

@tasks.route('/', methods=['GET','POST'])
def new_task():
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'POST':
            post_content = request.json
            response_http_code = task_handler.create(user_id, post_content.get("data"))
        elif request.method == 'GET':
            response = task_handler.get_all_tasks_and_todos(user_id)
            return ResponseHandler.construct_json_response(
                {
                    "http_code": response.get("http_code"),
                    "data": response.get("data")
                }
            )
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )

@tasks.route('<task_id>/', methods=['PUT', 'DELETE'])
def edit_or_delete_task(task_id):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        post_content = request.json
        if request.method == 'PUT':
            response_http_code = task_handler.edit(user_id, task_id, post_content.get("data"))
        elif request.method == 'DELETE':
            response_http_code = task_handler.delete(user_id, task_id)
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )

@tasks.route('/<task_id>/todos/', methods=['GET', 'POST'])
def new_todo(task_id):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        if request.method == 'POST':
            post_content = request.json
            response = todo_handler.create(user_id, task_id, post_content.get("data"))
        elif request.method == 'GET':
            response = todo_handler.get_all_todos(user_id, task_id)
    else:
        response["http_code"] = status.HTTP_403_FORBIDDEN

    if isinstance(response, int):
        return ResponseHandler.construct_json_response(
        {
            "http_code": response,
            "http_code_only": True
        })
    else:
        return ResponseHandler.construct_json_response(
        {
            "http_code": response.get("http_code"),
            "data": response.get("data")
        })

@tasks.route('<task_id>/todos/<todo_id>/', methods=['PUT', 'DELETE'])
def edit_or_delete_todo(task_id, todo_id):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        post_content = request.json
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
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )

@tasks.route('<task_id>/order-flag/<order_flag>/', methods=['PATCH'])
def toggle_order_flag(task_id, order_flag):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        response_http_code = task_handler.toggle_order_flag(user_id, task_id, order_flag)
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )

@tasks.route('<task_id>/todos/<todo_id>/toggle-done/', methods=['PATCH'])
def toggle_todo_done_flag(task_id, todo_id):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        post_content = request.json
        response_http_code = todo_handler.toggle_done(user_id, todo_id)
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )

@tasks.route('<task_id>/todos/<todo_id>/tags/<tag_name>/', methods=['PATCH', 'DELETE'])
def modify_todo_tag(task_id, todo_id, tag_name):
    user_id = DecodeToken.get_user_id(request.headers)
    if user_id is not None:
        todo_tags_handler = TodoTagsHandler()
        if request.method == "DELETE":
            response_http_code = todo_handler.delete_specific_tag({
                "user_id": user_id,
                "task_id": task_id,
                "todo_id": todo_id
            }, todo_tags_handler, tag_name)
        elif request.method == "PATCH":
            post_content = request.json
            response_http_code = todo_handler.edit_specific_tag({
                "user_id": user_id,
                "task_id": task_id,
                "todo_id": todo_id
            }, todo_tags_handler, {
                "old_tag": tag_name,
                "new_tag": post_content.get("data").get("new_name")
            })
    else:
        response_http_code = status.HTTP_403_FORBIDDEN

    return ResponseHandler.construct_json_response(
        {
            "http_code": response_http_code,
            "http_code_only": True
        }
    )
