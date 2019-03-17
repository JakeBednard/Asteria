from flask.views import View
from flask import jsonify


class RoutineView(View):

    def __init__(self, routine_obj):
        self.routine_obj = routine_obj
        self.name = self.routine_obj.routine_name

    methods = ['GET']

    def dispatch_request(self):
        # Get request handler.
        return jsonify(self.routine_obj.get_next_step())

