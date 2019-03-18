import os
from flask import Flask
from asteria.server.utilities.routine_view import RoutineView
from asteria.server.dashboard import dashboard
from asteria.mixins.base_routine import BaseRoutine
from asteria.server.builtin_routines.airplane_mode import AirplaneMode


class Asteria:

    def __init__(self, debug=True, port=5000, threaded=True, secret_key=None):

        # App Specific Settings
        self._routines = []

        # Flask Server Settings
        self._app = Flask(__name__)
        self._flask_debug = debug
        self._flask_port = port
        self._flask_threaded = threaded
        self._app.secret_key = secret_key if secret_key else os.urandom(64)

        # Attach Default Builtin Routines
        self.add_routine(AirplaneMode)

        # Register web browser view blueprint with flask server
        self._app.register_blueprint(dashboard.mod)

    def run(self):

        self._generate_routine_routes()

        #print("Registered Routes:")
        #print(self._app.url_map)

        # Launch the Flask server at localhost
        self._app.run(
            host='0.0.0.0',
            port=self._flask_port,
            threaded=self._flask_threaded,
            debug=self._flask_debug
        )

    def add_routine(self, routine):

        if issubclass(routine, BaseRoutine):
            self._routines.append(routine)
        else:
            # Make me a real exception.
            raise Exception("Routine provided is not of base type 'mixins.base_routine.BaseRoutine")

    def _generate_routine_routes(self):

        for routine in self._routines:

            routine_obj = routine()
            api_route = '/api/' + routine_obj.routine_name

            self._app.add_url_rule(
                rule=api_route,
                view_func=RoutineView.as_view(
                    name=routine_obj.routine_name,
                    routine_obj=routine_obj
                )
            )
