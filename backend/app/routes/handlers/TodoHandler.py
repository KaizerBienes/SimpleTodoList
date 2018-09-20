from app import db
from sqlalchemy import and_
from flask_api import status
from app.models import Task, Todo
import os
from datetime import datetime
from TodoTagsHandler import TodoTagsHandler
import logging

class TodoHandler:
    def create(self, user_id, task_id, todo_form):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.create_todo(user_id, task_id, todo_form)

    def create_todo(self, user_id, task_id, todo_form_details):
        task = self.get_task_record(user_id, task_id)
        if task is None:
            return status.HTTP_404_NOT_FOUND
        else:
            todo_due_date = self.format_date(todo_form_details.get("due_date", ""))
            if todo_due_date == status.HTTP_406_NOT_ACCEPTABLE:
                return status.HTTP_406_NOT_ACCEPTABLE
            else:
                todo = Todo(
                    task_id=task.id, \
                    description=todo_form_details.get("description", ""), \
                    due_date= todo_due_date\
                )

                db.session.add(todo)
                db.session.flush()
                self.add_todo_tags(user_id, todo.id, todo_form_details.get("tags", []))
                return self.commit_todo("create")

    def add_todo_tags(self, user_id, todo_id, tags):
        todo_tags_handler = TodoTagsHandler()
        if isinstance(tags, list):
            todo_tags_handler.add(user_id, todo_id, tags)
        elif isinstance(tags, str):
            todo_tags_handler.add(user_id, todo_id, [tags]) 

    def get_task_record(self, user_id, task_id):
        return Task.query.filter(and_(Task.user_id == user_id, Task.id == task_id)).first()

    def format_date(self, date):
        if date:
            try:
                return datetime.strptime(date, '%Y-%m-%d %H:%M %p')
            except ValueError:
                return status.HTTP_406_NOT_ACCEPTABLE
        else:
            return None

    def commit_todo(self, operation):
        try:
            db.session.commit()
            if operation == "create":
                return status.HTTP_201_CREATED
            else:
                return status.HTTP_202_ACCEPTED
        except Exception as e:
            logging.warn(e)
            db.session.rollback()
            db.session.flush()
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def edit(self, ids, todo_form):
        if ids.get("user_id", None) is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.edit_todo(ids, todo_form)

    def edit_todo(self, ids, todo_form_details):

        todo_due_date = self.format_date(todo_form_details.get("due_date", ""))
        if todo_due_date == status.HTTP_406_NOT_ACCEPTABLE:
            return status.HTTP_406_NOT_ACCEPTABLE
        else:
            todo = self.get_todo_record(ids)
            if todo:
                todo_tag_handler = TodoTagsHandler()
                todo_tag_handler.delete_all_tags_of_todo_id(todo.id)
                self.add_todo_tags(ids.get("user_id"), todo.id, todo_form_details.get("tags", []))
                
                setattr(todo, 'description', todo_form_details.get('description'))
                setattr(todo, 'due_date', todo_due_date)
                return self.commit_todo("edit")
            else:
                logging.warn("Cant edit todo. Perhaps there is no todo")
                return status.HTTP_404_NOT_FOUND

    def get_todo_record(self, ids):
        task = Task.query.filter(and_(Task.user_id == ids.get("user_id"), Task.id == ids.get("task_id"))).first()
        if task is None:
            return None
        else:
            return Todo.query.filter(and_(Todo.task_id == task.id, Todo.id == ids.get("todo_id"))).first()

    def delete(self, ids):
        if ids.get("user_id", None) is None or ids.get("task_id", None) is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.delete_todo(ids)

    def delete_todo(self, ids):
        todo = self.get_todo_record(ids)
        if todo:
            db.session.delete(todo);
            return self.commit_todo("delete")
        else:
            logging.warn("Cant delete todo. Perhaps there is no todo")
            return status.HTTP_404_NOT_FOUND

    def get_all_todos(self, user_id, task_id):
        task = self.get_task_record(user_id, task_id)
        if task is None:
            return {
                "http_code": status.HTTP_404_NOT_FOUND
            }
        else:
            todos = Todo.query.filter(Todo.task_id == task.id).all()
            todo_list = []
            for todo in todos:
                todo_tags_handler = TodoTagsHandler()
                todo_object = {
                    "id": todo.id,
                    "description": todo.description,
                    "due_date": todo.due_date.strftime('%Y-%m-%d %H:%M %p'),
                    "updated_date": todo.updated_date.strftime('%Y-%m-%d %H:%M %p'),
                    "tags": todo_tags_handler.get_all_tags_from_todo_id(todo.id)
                }
                todo_list.append(todo_object)

            return {
                "http_code": status.HTTP_202_ACCEPTED,
                "data": todo_list
            }
