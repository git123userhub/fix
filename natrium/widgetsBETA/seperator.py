from natrium import widgetsBETA
import pygame

class Seperator(widgetsBETA.Widget):
    def __init__(self, container, length, orient='horizontal', color='grey'):
        size = (length, 1) if orient == 'horizontal' else (1, length)
        style = {
            'cornerradius':1,
            'borderwidth':0,

            'background':color,
            'bordercolor':'white',

            'gradial_orient':'horizontal',
            'gradient_blend':10
        }

        super().__init__(container, padding=(0, 0), size=size, style=style)

    def render_hierarchy(self):
        line = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32) # ez
        line.fill(self.style['background'])

        return line

    def place_hierarchy(self):
        self.blit(self._base_hierarchy_rendering, (0, 0))