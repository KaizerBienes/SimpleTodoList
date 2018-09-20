from app import db
from sqlalchemy import and_
from flask_api import status
from app.models import UserCredential, Task, Todo, TodoTag, Tag
from heapq import nlargest
import os
from datetime import datetime
import logging

class TagsHandler:
    def create(self, user_id, tag_form):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            return self.create_tag(tag_form.get("name", None))

    def create_tag(self, tag_name):
        tag_found = self.get_tag_record(tag_name)
        if tag_found is not None:
            # Existing tags are fine
            return status.HTTP_202_ACCEPTED
        else:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            return self.commit_tag()

    def get_tag_record(self, tag_name):
        return Tag.query.filter(Tag.name == tag_name).first()

    def commit_tag(self):
        try:
            db.session.commit()
            return status.HTTP_202_ACCEPTED
        except Exception as e:
            logging.warn(e)
            db.session.rollback()
            db.session.flush()
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_tags(self):
        tags = Tag.query.filter().all()
        tags_list = []
        for tag in tags:
            tags_list.append(tag.name)

        return {
            "http_code": status.HTTP_202_ACCEPTED,
            "data": tags_list
        }

    def get_top_tags(self, user_id, top_count):
        top_tags = (db.session.query(UserCredential, Task, Todo, TodoTag, Tag)
            .filter(UserCredential.id == user_id)
            .filter(UserCredential.id == Task.user_id)
            .filter(Task.id == Todo.task_id)
            .filter(Todo.id == TodoTag.todo_id)
            .filter(TodoTag.tag_id == Tag.id)
            .all())
        
        tag_counter = {}
        for todo_tag_record in top_tags:
            tag_name = todo_tag_record.Tag.name
            logging.warn(tag_name)
            if not tag_name in tag_counter:
                tag_counter[tag_name] = 1
            else:
                tag_counter[tag_name] += 1
        
        top_tags = nlargest(int(top_count), tag_counter, key=tag_counter.get)
        return {
            "http_code": status.HTTP_202_ACCEPTED,
            "data": { "top_tags": top_tags }
        }
