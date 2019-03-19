from asteria.mixins.color_palette_routine import ColorPaletteRoutine


class TestMode(ColorPaletteRoutine):

    def __init__(self):
        """Color routine that's like flying inside of a 787."""

        routine_name = 'test_mode'
        num_color_channels = 2
        transition_time = 100  # milliseconds

        color_palette = [
            {
                'name': 'Blue',
                'rgb': (0, 20, 255)
            },
            {
                'name': 'Purple',
                'rgb': (102, 0, 255)
            },
            {
                'name': 'Green',
                'rgb': (225, 255, 0)
            },
            {
                'name': 'Orange',
                'rgb': (255, 204, 0)
            },
            {
                'name': 'Pink',
                'rgb': (204, 0, 173)
            },
        ]

        super().__init__(
            color_palette=color_palette,
            routine_name=routine_name,
            num_color_channels=num_color_channels,
            do_not_repeat=True,
            default_transition_time=transition_time
        )
