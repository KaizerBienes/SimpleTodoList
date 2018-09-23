from app import db
from sqlalchemy.sql import func, expression

class UserCredential(db.Model):
    __tablename__ = 'user_credential'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    task = db.relationship('Task', backref='task_user_credential', lazy='dynamic')

    def __repr__(self):
        return '<UserCredential {}>'.format(self.username)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_credential.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    updated_date = db.Column(db.DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    order_by_flag = db.Column(db.Boolean, nullable=False, server_default=expression.false())
    todo = db.relationship('Todo', backref='todo_task', lazy='dynamic')

    def __repr__(self):
        return '<Task {}>'.format(self.title)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime)
    done_flag = db.Column(db.Boolean, nullable=False, server_default=expression.false())
    updated_date = db.Column(db.DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    todo_tag = db.relationship('TodoTag', backref='todo_tag_todo', lazy='dynamic')

    def __repr__(self):
        return '<Todo {}>'.format(self.description)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    todo_tag = db.relationship('TodoTag', backref='todo_tag_tag', lazy='dynamic')

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

class TodoTag(db.Model):
    __tablename__ = 'todo_tag'
    __table_args__ = (
        db.UniqueConstraint('todo_id', 'tag_id', name='unique_todo_tag_combination'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<TodoTag {}>'.format(self.tag_id + "_" + self.todo_id)
