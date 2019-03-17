import random

from asteria.mixins.base_routine import BaseRoutine


class ColorPaletteRoutine(BaseRoutine):
    """Use this object to construct color palettes to display. Built upon BaseRoutine."""

    def __init__(self, color_palette=None, routine_name=None, num_color_channels=1,
                 do_not_repeat=True, default_transition_time=100, cache_hold_time=80):
        """Use this object to construct color palettes to display. Built upon BaseRoutine.

        Args:
            color_palette:
                List containing containing Dicts of color info with 'color_name' and color_rgb (a
                tuple of a RGB color to display). If no palette is provide, exception 'ColorPaletteNotDefined'
                will be thrown.
                Example:
                    [
                        {
                            'color_name': 'fantastic_blue',
                            'color_rgb': (10,20,250)
                        },
                        ...
                    ]
            routine_name:
                Name for the routine to be referenced by. Default is a random 64-char ASCII string.
            num_color_channels:
                Integer number of colors to return per step. Each color can be considered a
                channel. Default is 1.
            do_not_repeat:
                When True, we'll make sure each color channel does not repeat the previous
                color assigned to this color channel.
            default_transition_time:
                Integer for the amount milliseconds for the default transition
                time for light change commands. Default is 100ms.
            cache_hold_time:
                Integer for the amount of milliseconds to cache the current color
                setting for. This is cut down on the amount of calculations needed when serving
                multiple clients. By default, this will be 80% of default_transition_time.

        Returns:
            BaseColorSwitcher object
        """

        super().__init__(
            routine_name=routine_name,
            default_transition_time=default_transition_time,
            cache_hold_time=cache_hold_time
        )

        if color_palette is None:
            raise self.ColorPaletteNotDefined(self.routine_name)

        self.color_palette = color_palette
        self.num_color_channels = num_color_channels
        self.do_not_repeat = do_not_repeat
        self.current_color_channels = None

    def get_next_step(self):
        """Get next color channels(s) for display.

        Returns:
            num_of_colors sized list of dicts containing color information.
            Example:
                [
                    {
                        'color_name': 'fantastic_blue',
                        'color_rgb': (10,20,250)
                    },
                    ...
                ]
        """

        next_color_channels = []
        for i in range(self.num_color_channels):

            random_seed = random.randint(0, len(self.color_palette) - 1)
            color_picked = self.color_palette[random_seed]

            # This bit of logic is to prevent color channels from repeating
            # colors when self.do_not_repeat is True.
            if self.current_color_channels is not None:
                if self.do_not_repeat and len(self.color_palette) > 1:
                    while color_picked == self.current_color_channels[i]:
                        random_seed = random.randint(0, len(self.color_palette) - 1)
                        color_picked = self.color_palette[random_seed]

            next_color_channels.append(color_picked)

        self.current_color_channels = next_color_channels

        return next_color_channels

    class ColorPaletteNotDefined(Exception):
        """We throw this when a color palette is defined on init."""
        def __init__(self, routine_name=''):
            super().__init__(
                'Error: Color Palette has not not been defined for routine: "{}".'.format(routine_name)
            )
