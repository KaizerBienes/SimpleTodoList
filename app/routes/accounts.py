from flask import Blueprint
from flask import render_template
from flask import request, jsonify
import logging

accounts = Blueprint('accounts', __name__, template_folder='templates')
