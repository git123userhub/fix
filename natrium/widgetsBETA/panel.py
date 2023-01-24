from natrium import widgetsBETA, common, graphics, display
import pygame

default_style = {
    'cornerradius':4,
    'borderwidth': 1,

    'background':'#EFEFEF',
    'bordercolor':'grey55',

    'gradial_orient': 'horizontal',
    'gradient_blend': 10
}

class Panel(widgetsBETA.Widget):
    def __init__(self, container, style=None, size=(400, 300), padding=(10, 10)):

        style = style if style else default_style

        super().__init__(container, style, size, padding)

        self._children = []

    def blit_wid(self, widget, position):
        self._children.append((widget, position))

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy()]

        for child, position in self._children:
            self._hierarchy_rendering[2].blit(child, position)

        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

    def absolute_placement(self, x, y):
        super().absolute_placement(x, y)
        self._children = []