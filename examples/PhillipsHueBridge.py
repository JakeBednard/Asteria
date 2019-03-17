import requests
from phue import Bridge
from time import sleep
from rgbxy import Converter


def calc_brightness(red, green, blue):
    color_sum = red + green + blue
    bri = int(color_sum / 3)
    bri = 254 if bri >= 255 else bri
    bri = 100 if bri < 100 else bri
    return bri

def calc_night_brightness(color, min=0, max=20):
    color_sum = color['red'] + color['green'] + color['blue']
    bri = int(color_sum / 3)
    bri = max if bri > max else bri
    bri = min if bri < min else bri
    return bri

def color_bounding(color_value):
    """Phue has a built divide by zero error"""
    if color_value < 1:
        color_value = 1
    elif color_value > 254:
        color_value = 254
    return color_value

color_converter = Converter()

bridge = Bridge('192.168.1.149')

bridge.connect()

while True:

    try:
        r = requests.get('http://localhost:5000/api/airplane')
        colors = r.json()
        number_of_lights = 1

        if number_of_lights == 1:
            color = colors[0]

            red = color_bounding(color['rgb'][0])
            green = color_bounding(color['rgb'][1])
            blue = color_bounding(color['rgb'][2])

            xy_color = color_converter.rgb_to_xy(red, green, blue)
            brightness = calc_brightness(red, green, blue)

            print('Current Color:', color['name'])

            bridge.set_light([1,2,3,4], {
                'xy': xy_color,
                'bri': brightness,
                'transitiontime': 100
            })

            sleep(10)

        # elif number_of_lights == 4:
        #     for i in range(number_of_lights):
        #
        #         rgb_color = rgb_colors[i % len(rgb_colors)]
        #         xy_color = color_converter.rgb_to_xy(rgb_color['red'], rgb_color['green'], rgb_color['blue'])
        #         brightness = calc_brightness(rgb_color)
        #
        #         print('Current Color:', rgb_color, xy_color, brightness)
        #
        #         bridge.set_light([i+1], {
        #             'xy': xy_color,
        #             'bri': brightness,
        #             'transitiontime': 1}
        #         )
        #
        #         sleep(0.1)
        #
        #     sleep(1)

        else:
            sleep(1)

    except Exception as e:
        raise e

