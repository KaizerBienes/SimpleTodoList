from app import db
from sqlalchemy import and_
from flask_api import status
from app.models import Task
import os
import datetime
import logging

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
        return self.commit_task()


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
            return self.commit_task()
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
            db.session.delete(task);
            return self.commit_task()
        else:
            logging.warn("Cant delete task. Perhaps there is no task")
            return status.HTTP_404_NOT_FOUND

    def get_task_record(self, user_id, task_id):
        return Task.query.filter(and_(Task.user_id == user_id, Task.id == task_id)).first()

    def commit_task(self):
        try:
            db.session.commit()
            return status.HTTP_202_ACCEPTED
        except Exception as e:
            logging.warn(e)
            db.session.rollback()
            db.session.flush()
            return status.HTTP_500_INTERNAL_SERVER_ERROR
