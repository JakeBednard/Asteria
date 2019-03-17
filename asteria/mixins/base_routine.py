from string import ascii_letters
from random import choice


class BaseRoutine:
    """Base object to build light changing routines upon"""

    def __init__(self, routine_name=None, default_transition_time=100, cache_hold_time=None):
        """Base object to build light changing routines upon.

        Args:
            routine_name:
                Name for the routine to be referenced by. Default is a random 64-char ASCII string.
            default_transition_time:
                Integer for the amount milliseconds for the default transition
                time for light change commands. Default is 100ms.
            cache_hold_time:
                Integer for the amount of milliseconds to cache the current color
                setting for. This is cut down on the amount of calculations needed when serving
                multiple clients. By default, this will be 80% of default_transition_time.

        Returns:
            BaseRoutine object.
        """

        if routine_name is None:
            self.routine_name = ''.join([choice(ascii_letters) for _ in range(64)])
        else:
            self.routine_name = routine_name.strip().replace(' ', '_')

        self.default_transition_time = 0 if default_transition_time < 0 else default_transition_time

        if cache_hold_time is None or cache_hold_time < 0:
            self.cache_hold_time = int(0.8 * default_transition_time)
        else:
            self.cache_hold_time = cache_hold_time

    def get_next_step(self):
        raise NotImplementedError()
