from app import db
from flask_api import status
from app.models import Todo, TodoTag, Tag
from TagsHandler import TagsHandler
from heapq import nlargest

class TodoTagsHandler:
    def add(self, user_id, todo_id, tags):
        if user_id is None:
            return status.HTTP_403_FORBIDDEN
        else:
            for tag_name in tags:
                self.create_todo_tag(user_id, todo_id, tag_name)

    def create_todo_tag(self, user_id_from_form, todo_id_from_form, tag_name):
        tags_handler = TagsHandler()
        self.create_tag_if_not_exists(user_id_from_form, tags_handler, tag_name)
        todo_tag = TodoTag(
            todo_id=todo_id_from_form,
            tag_id=tags_handler.get_tag_record(tag_name).id
        )

        db.session.add(todo_tag)


    def create_tag_if_not_exists(self, user_id, tags_handler, tag):
        tag_record = tags_handler.get_tag_record(tag)
        if tag_record is None:
            tags_handler.create(user_id, { "name": tag })

    def get_all_tags_from_todo_id(self, todo_id):
        todo_tag_join = (db.session.query(Todo, TodoTag, Tag)
            .filter(Todo.id == todo_id)
            .filter(Todo.id == TodoTag.todo_id)
            .filter(TodoTag.tag_id == Tag.id)
            .all())
        
        tags = []
        for todo_tag_record in todo_tag_join:
            tags.append(todo_tag_record.Tag.name)
        return tags

    def delete_all_tags_of_todo_id(self, todo_id):
        todo_tag_join = (db.session.query(Todo, TodoTag, Tag)
            .filter(Todo.id == todo_id)
            .filter(Todo.id == TodoTag.todo_id)
            .filter(TodoTag.tag_id == Tag.id)
            .all())
        
        tags = []
        for todo_tag in todo_tag_join:
            self.delete_todo_tag(todo_tag.TodoTag.id)
        return tags

    def delete_todo_tag(self, todo_tag_id):
        todo_tag_record = self.get_todo_tag_record(todo_tag_id)
        db.session.delete(todo_tag_record)
        return self.commit_todo_tag("delete")

    def get_todo_tag_record(self, todo_tag_id):
        todo_tag_record = TodoTag.query.filter(TodoTag.id == todo_tag_id).first()
        return todo_tag_record

    def commit_todo_tag(self, operation):
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
