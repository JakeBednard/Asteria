"""
This file contains all operations related to index page
"""

from flask import Blueprint
from flask import jsonify
from flask import render_template


mod = Blueprint('index', __name__)


@mod.route('/', methods=['GET'])
def index():
    return render_template("browser.html")
