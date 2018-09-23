from app import app
from flask import Blueprint
from flask import render_template
import sys

sys.path.insert(0, "app/routes/")
sys.path.insert(1, "app/routes/handlers/")

from accounts import accounts
from tasks import tasks
from todos import todos
from tags import tags


app.register_blueprint(accounts, url_prefix='/api/accounts')
app.register_blueprint(tasks, url_prefix='/api/tasks')
app.register_blueprint(todos, url_prefix='/api/todos')
app.register_blueprint(tags, url_prefix='/api/tags')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
