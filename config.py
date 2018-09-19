import os
base_directory = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_directory, 'simple_todo_list.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
