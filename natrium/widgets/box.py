import pygame
from natrium import graphics, widgets, common, display

pygame.init()

def get_abs_pos(widget, offset=None):
    if not offset: offset = [0, 0]
    add_to_offset =[widget['borderwidth']+x for x in widget.relpos] if not isinstance(widget, display.Window) else [0, 0]
    offset = [offset[0]+add_to_offset[0], offset[1]+add_to_offset[1]]

    if not isinstance(widget, display.Window):
        if not isinstance(widget.master, display.Window):
            get_abs_pos(widget.master, offset)

    return offset

class Box(pygame.Surface):
    instance_array = []

    def __init__(self, master, size, position, anchor, style):
        super().__init__([x+2 for x in size], pygame.SRCALPHA, 32)

        self.master = master
        anchor_calc = common.anchor_calculation(self.master, self, anchor, *position)
        self.rect = pygame.Rect(
                                [x+y for x, y in
                                 zip(get_abs_pos(self.master), anchor_calc)
                                 ],
                                size)

        self.relpos = anchor_calc
        self.anchor = anchor

        self.style = style.copy()
        self._render_style = self._return_rendering()
        self.size = size

        Box.instance_array.append(self)

    def _return_rendering(self):
        pos = [self['borderwidth']]*2
        size = [x-self['borderwidth']*2 for x in self.rect.size]

        main_body = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self['background'], self['cornerradius'],
                                                      orient=self['gradial_orient'],
                                                      gradient_blend=self['gradient_blend'])
        bordercolor = (0, 0, 0, 0) if not self['borderwidth'] else self['bordercolor']

        border_rect = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                        self['cornerradius'], orient=self['gradial_orient'],
                                                        gradient_blend=self['gradient_blend'])

        return [main_body, border_rect]

    def _render(self):
        pos = [self['borderwidth']]*2

        self.blit(self._render_style[1], (0, 0))
        self.blit(self._render_style[0], pos)

    def place(self):
        self.fill((0, 0, 0, 0))
        self._render()

        if not isinstance(self.master, (display.Window, widgets.Panel)): self.master.blit(self, self.relpos)
        else: self.master.blit_wid(self, self.relpos)

        self.rect = pygame.Rect(
            [x+y for x, y in
             zip(get_abs_pos(self.master), self.relpos)
             ],
            self.rect.size)

    def is_hover(self, mpos):
        return self.rect.collidepoint(*mpos)

    @classmethod
    def any_active(cls, mpos):
        return any([inst.is_hover(mpos)
                    for inst in cls.instance_array
                    if isinstance(inst, (widgets.Button, widgets.InputBox, widgets.ToggleButton, widgets.Slider))])

    def __getitem__(self, item):
        return self.style[item]

    def __setitem__(self, key, value):
        self.style[key] = value


