import pygame
from natrium import widgetsBETA, common

default_style = {
    'grip_cornerradius':4,
    'grip_borderwidth':1,

    'bar_borderwidth':1,

    'bar_background':'grey',
    'bar_bordercolor':'grey33',

    'grip_background':'dodgerblue3',
    'grip_hover_bg':'dodgerblue2',
    'grip_active_bg':'dodgerblue',

    'grip_bordercolor':'skyblue',
    'grip_hover_bc':'skyblue2',
    'grip_active_bc':'skyblue3',

    'grip_gradial_orient':'horizontal',
    'grip_gradient_blend':10

}

class HorizontalSlider(widgetsBETA.Widget):
    def __init__(self, container, length=300, grip_size=(30, 40), style=None, min_value=0, max_value=100):

        style = style if style else default_style

        box_style = {
            'cornerradius':1,
            'borderwidth': style['bar_borderwidth'],

            'background': style['bar_background'],
            'bordercolor': style['bar_bordercolor'],

            'gradial_orient':'horizontal',
            'gradient_blend': 1
        }

        grip_style = {
            'cornerradius': style['grip_cornerradius'],
            'borderwidth': style['grip_borderwidth'],

            'background': style['grip_background'],
            'hover_bg': style['grip_hover_bg'],
            'active_bg': style['grip_active_bg'],

            'foreground': (0, 0, 0, 0),
            'hover_fg': (0, 0, 0, 0),
            'active_fg': (0, 0, 0, 0),

            'bordercolor': style['grip_bordercolor'],
            'hover_bc': style['grip_hover_bc'],
            'active_bc': style['grip_active_bc'],

            'gradial_orient': style['grip_gradial_orient'],
            'gradient_blend': style['grip_gradient_blend']
        }

        super().__init__(container, box_style, size=(4, length), padding=(0, 0))

        self.grip = widgetsBETA.Button(self.container, style=grip_style, size=grip_size, padding=(0, 0))

        self.min_value = min_value
        self.max_value = max_value

        self._value = 0

        self._is_hover = False
        self._is_click = False

        self._active = False

        self._horizontal_offset = 0

    def trigger(self, mpos, mprd):


    def absolute_placement(self, x, y):...

