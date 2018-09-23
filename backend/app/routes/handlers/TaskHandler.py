from app import db
from sqlalchemy import and_
from flask_api import status
from app.models import Task, Todo
import os
from datetime import datetime
import logging
from TodoHandler import TodoHandler

class TaskHandler:
    def create(self, user_id, task_form):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.create_task(task_form, user_id)

    def create_task(self, task_form_details, tokenized_user_id):
        task = Task(
            user_id=tokenized_user_id, \
            title=task_form_details.get("title", ""), \
            description=task_form_details.get("description", "")
        )

        db.session.add(task)
        return self.commit_task("create")


    def edit(self, user_id, task_id, task_form):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.edit_task(user_id, task_id, task_form)

    def edit_task(self, tokenized_user_id, task_id_from_form, task_form):
        task = self.get_task_record(user_id=tokenized_user_id, task_id=task_id_from_form)

        if task:
            setattr(task, 'title', task_form.get('title'))
            setattr(task, 'description', task_form.get('description'))
            return self.commit_task("edit")
        else:
            logging.warn("Cant delete task. Perhaps there is no task")
            return status.HTTP_404_NOT_FOUND

    def delete(self, user_id, task_id):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.delete_task(user_id, task_id)

    def delete_task(self, user_id, task_id):
        task = self.get_task_record(user_id, task_id)
        if task:
            todos = Todo.query.filter(and_(Todo.task_id == task_id)).all()
	    for todo in todos:
		db.session.delete(todo)
            db.session.delete(task)
            return self.commit_task("delete")
        else:
            logging.warn("Cant delete task. Perhaps there is no task")
            return status.HTTP_404_NOT_FOUND

    def get_task_record(self, user_id, task_id):
        return Task.query.filter(and_(Task.user_id == user_id, Task.id == task_id)).first()

    def commit_task(self, operation):
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

    def get_all_tasks_and_todos(self, user_id):
        todo_handler = TodoHandler()
        tasks = Task.query.filter(Task.user_id == user_id).all()
        task_list = []
        for task in tasks:
            task_object = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "updated_date": task.updated_date.strftime('%Y-%m-%d %H:%M'),
                "todos": todo_handler.get_all_todos(user_id, task.id).get("data", [])
            }
            task_list.append(task_object)

        return {
            "http_code": status.HTTP_202_ACCEPTED,
            "data": task_list
        }

    def toggle_order_flag(self, user_id, task_id, order_by_flag):
        task = self.get_task_record(user_id, task_id)
        if task:
            if order_by_flag == '0':
                setattr(task, 'order_by_flag', 0)
            elif order_by_flag == '1':
                setattr(task, 'order_by_flag', 1)

            return self.commit_task("edit")
        else:
            logging.warn("Cant delete task. Perhaps there is no task")
            return status.HTTP_404_NOT_FOUND

