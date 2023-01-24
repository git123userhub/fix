import pygame
from natrium import graphics, display, widgetsBETA

def get_abs_pos(widget, offset=None):
    offset = offset if offset else [0, 0]

    if not isinstance(widget, display.Window):
        offset = [x+y+(z//2+1) for x, y, z in zip(offset, widget._absolute_pos, widget._padding)]

        if not isinstance(widget.container, display.Window):
            get_abs_pos(widget.container, offset=offset)

    return offset

class Widget(pygame.Surface):
    instances = []
    interactives = []

    def __init__(self, container, style, size=(100, 50), padding=(10, 10)):
        sizepadding = [x+y for x, y in zip(size, padding)]

        super().__init__([x+2 for x in sizepadding], pygame.SRCALPHA, 32)
        self.convert()

        self._base_size = size
        self._padding = padding

        self.rect = pygame.Rect((-1000, 0), sizepadding)
        self.container = container
        self.style = style

        self._relative_pos = (-1000, 0)
        self._absolute_pos = (-1000, 0)
        self._base_hierarchy_rendering = self.render_hierarchy()
        self._hierarchy_rendering = None
        self._isplaced = False

        Widget.instances.append(self)
        if isinstance(self, (widgetsBETA.Button, widgetsBETA.InputBox, widgetsBETA.ToggleButton,
                             widgetsBETA.RadioButton)):
            Widget.interactives.append(self)

    def render_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        size = [x-self.style['borderwidth']*2 for x in self.rect.size]

        padding = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self.style['background'], self.style['cornerradius'],
                                                    orient=self.style['gradial_orient'],
                                                    gradient_blend=self.style['gradient_blend'])
        content = pygame.Surface(self._base_size, pygame.SRCALPHA, 32)
        padding.blit(content, [x//2-y//2-1 for x, y in zip(self.rect.size, self._base_size)])

        bordercolor = (0, 0, 0, 0) if not self.style['borderwidth'] else self.style['bordercolor']

        border = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                   self.style['cornerradius'], orient=self.style['gradial_orient'],
                                                   gradient_blend=self.style['gradient_blend'])

        return [padding, border, content]

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy()]

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

    def absolute_placement(self, x, y):
        if self._relative_pos != (x, y):
            self._relative_pos = (x, y)
            if isinstance(self.container, display.Window):
                self._absolute_pos = self._relative_pos
            else:
                self._absolute_pos = [x+y for x, y in zip(self._relative_pos, get_abs_pos(self.container))]

        if self.rect != pygame.Rect(self._absolute_pos, self.rect.size):
            self.rect = pygame.Rect(self._absolute_pos, self.rect.size)

        self.place_hierarchy()

        self.container.blit_wid(self, self._relative_pos)