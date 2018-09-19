from app import app
from flask import Blueprint
from flask import render_template
import sys

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', route_page="Routes")

sys.path.insert(0, "app/routes/")
from accounts import accounts
from tasks import tasks
from todos import todos
from tags import tags

app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(tasks, url_prefix='/tasks')
app.register_blueprint(todos, url_prefix='/todos')
app.register_blueprint(tags, url_prefix='/tags')
