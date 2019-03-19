"""
"""

from flask import Blueprint
from flask import render_template


def dashboard_factory(routines):
    """Create a dashboard blueprint to be be served by flask for browser testing.

    This isn't my favorite way to do this, but importing the app context would cause
    a circular dependency. This can be revisited later if any ideas come up.
    """

    mod = Blueprint('index', __name__, template_folder='template')

    @mod.route('/', methods=['GET'])
    def index():
        return render_template("dashboard.html", routines=routines)

    return mod
