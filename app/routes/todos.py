from flask import Blueprint
from flask import render_template
from flask import request, jsonify
import logging

todos = Blueprint('todos', __name__, template_folder='templates')
