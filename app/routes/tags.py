from flask import Blueprint
from flask import render_template
from flask import request, jsonify
import logging

tags = Blueprint('tags', __name__, template_folder='templates')
