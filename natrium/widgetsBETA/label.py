from natrium import widgetsBETA, common
import pygame

default_style = {
    'cornerradius':4,
    'borderwidth':0,

    'background':(0, 0, 0, 0),
    'foreground':'black',
    'bordercolor':(0, 0, 0, 0),

    'gradial_orient':'horizontal',
    'gradient_blend': 10
}

class Label(widgetsBETA.Widget):
    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val
        self._base_text_rendering = pygame.font.SysFont(*self._font_data).render(self._text, 1, self.style['foreground'])

    def __init__(self, container, style=None, text="", font=('gadugi', 15), anchor='topleft', size=(100, 50), padding=(10, 10)):

        style = style if style else default_style

        super().__init__(container, style, size, padding)
        self._text = text
        self.text_anchor = anchor

        self._font_data = font
        self._base_text_rendering = pygame.font.SysFont(*font).render(self._text, 1, self.style['foreground'])
        self._text_rendering = None

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy()]
        self._text_rendering = self._base_text_rendering.copy()

        text_position = common.anchor_calculation(
            self._hierarchy_rendering[2],
            self._text_rendering,
            self.text_anchor,
            0,
            0
        )

        self._hierarchy_rendering[2].blit(self._text_rendering, text_position)
        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)
