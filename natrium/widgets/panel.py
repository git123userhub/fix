from natrium import widgets, graphics
import pygame

class Panel(widgets.Box):
    def __init__(self, master, size, position, style, anchor):
        if style['widget'] != 'Panel':
            raise ValueError(f"Panel does not support style of widget {style['widget']}")

        self.child_list = []
        super().__init__(master, size, position, anchor, style)
        self._const_render_style = self._return_rendering()

    def blit_wid(self, widget, destination):
        self.child_list.append([widget, destination])
        print(self.child_list)

    def _return_rendering(self):
        pos = [self['borderwidth']]*2
        size = [x-self['borderwidth']*2 for x in self.rect.size]

        main_body = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self['background'], self['cornerradius'],
                                                      orient=self['gradial_orient'],
                                                      gradient_blend=self['gradient_blend'])

        border_rect = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), self['bordercolor'],
                                                        self['cornerradius'], orient=self['gradial_orient'],
                                                        gradient_blend=self['gradient_blend'])

        return [main_body, border_rect]

    def return_children(self):
        return self.child_list

    def place(self):
        self._render_style = [self._const_render_style[0].copy(), self._const_render_style[1].copy()]

        for child in self.child_list:
            print(child[0], child[1], 12)
            self._render_style[0].blit(child[0], child[1])

        pos = [self['borderwidth']]*2
        self.blit(self._render_style[1], [0, 0])
        self.blit(self._render_style[0], pos)

        if isinstance(self.master, pygame.Surface): self.master.blit(self, self.relpos)
        else: self.master.blit_wid(self, self.relpos)

        self.rect = pygame.Rect(
            [x+y for x, y in
            zip(self.master.get_abs_offset(), self.relpos)
            ],
            self.rect.size)
        self.child_list = []

    # def _render(self):
    #     render_rect = self._return_rendering()
    #
    #     render_rect[1].draw()
    #     render_rect[0].draw()
