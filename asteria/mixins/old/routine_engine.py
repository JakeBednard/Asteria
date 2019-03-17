import time
import mss

from asteria.server.routines.mapping import routine_mapping


class RoutineEngine:

    def __init__(self, x_padding_percent=0, y_padding_percent=0):
        self._bounding_box = self._calculate_bounding_box(x_padding_percent, y_padding_percent)
        self.current_routine_name = None
        self.routine_mapping = routine_mapping

    def set_routine(self, next_routine_name=None):

        if next_routine_name is None:
            return

        if next_routine_name in self.routine_mapping:
            self.current_routine_name = next_routine_name
            return True

        print("Error: routine not found. Not changing routine. Routine Submitted: {} ".format(next_routine_name))
        return False

    def get_next_step(self):
        routine_name = self.current_routine_name
        if routine_name in self.routine_mapping:
            current_routine = self.routine_mapping[routine_name]
            return current_routine.get_next_step()

        return False

    def performance_test(self, iterations=100):

        self.set_routine(next_routine_name='airplane_mode')

        iter_count = 0
        start = time.time()

        while iter_count < iterations:
            current_color = self.get_next_step()
            print(current_color)
            iter_count += 1

        end = time.time()

        elapsed = end - start
        iterations_per_sec = int(iter_count / elapsed)

        return iterations_per_sec

    @staticmethod
    def _calculate_bounding_box(x_padding_percent, y_padding_percent):

        with mss.mss() as sct:
            monitor = sct.monitors[-1]

            left = monitor["left"] + monitor["width"] * x_padding_percent // 200
            top = monitor["top"] + monitor["height"] * y_padding_percent // 200
            right = (monitor["left"] + monitor["width"]) - (monitor["width"] * x_padding_percent // 200)
            bottom = (monitor["top"] + monitor["height"]) - (monitor["height"] * y_padding_percent // 200)

            bounding_box = (left, top, right, bottom)

        return bounding_box


if __name__ == '__main__':
    test_object = RoutineEngine(50, 50)
    iterations_per_second = test_object.performance_test(iterations=100)
    print(str(iterations_per_second) + " iterations per second.")
