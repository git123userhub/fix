import pygame
import sys
from natrium import widgets, graphics, widgetsBETA
from natrium.typehinting import *

class Window:
    @property
    def size(self):
        return self._disp.get_size()

    @property
    def width(self):
        return self._disp.get_width()

    @property
    def height(self):
        return self._disp.get_height()

    def __init__(self, size, background, gradial_orient='horizontal',
                 gradient_blend, title:str = "Window", icon:str = None, resizable:bool = True):
        flags = pygame.SRCALPHA
        if resizable:
            flags |= pygame.RESIZABLE

        self._disp = pygame.display.set_mode(size, flags)
        pygame.display.set_caption(title)
        self.master = None

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))

        self.background = background
        self.gradial_orient = gradial_orient
        self.gradient_blend = gradient_blend

        self._clock = pygame.time.Clock()
        self._events = []
        self._mpos = (0, 0)
        self._mprd = None
        self._rect = None
        self._previous_size = 0
        self._z_event_index = 0

    def trigger(self):
        self._events = pygame.event.get()
        self._mpos = pygame.mouse.get_pos()
        self._mprd = pygame.mouse.get_pressed()

        for event in self._events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not isinstance(self.background, (list, tuple)):
            self._disp.fill(self.background)

        if isinstance(self.background, (list, tuple)):
            if self._previous_size != self.size:
                self._rect = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.size),
                                                               self.background,
                                                               radius=1, orient=self.gradial_orient,
                                                               gradient_blend=self.gradient_blend)
            self._disp.blit(self._rect, (0, 0))

        self._previous_size = self.size

    def listen(self, widget):
        params = []

        if isinstance(widget, (widgets.InputBox, widgets.Button, widgets.ToggleButton,
                               widgetsBETA.Button, widgetsBETA.InputBox, widgetsBETA.ToggleButton,
                               widgetsBETA.RadioButton, widgetsBETA.Listbox, widgetsBETA.Spinbox)):
            params.append(self._events)

        params.append(self._mpos)

        if isinstance(widget, (widgets.Button, widgets.Slider, widgetsBETA.Button,
                               widgetsBETA.Spinbox)):
            params.append(self._mprd)

        widget.trigger(*params)

    def listen_multiple(self, widgets):
        for widget in widgets:
            self.listen(widget)

    def time_since_process(self):
        return pygame.time.get_ticks() / 1000

    def get_abs_offset(self):
        return self._disp.get_abs_offset()

    def get_offset(self):
        return self._disp.get_offset()

    def blit_wid(self, surf, dest):
        self._disp.blit(surf, dest)

    def get_rate(self):
        return self._clock.get_fps()

    def refresh(self):
        pygame.display.flip()
        self._clock.tick(222)
