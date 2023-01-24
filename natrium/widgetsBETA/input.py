import pygame
from natrium import widgetsBETA, graphics, common

default_style = {
    'cornerradius':4,
    'borderwidth':1,

    'background':'#FAFAFA',
    'active_bg':'#FAFAFA',

    'foreground':'black',
    'active_fg':'black',

    'bordercolor':'grey55',
    'active_bc':'dodgerblue',

    'gradial_orient':'horizontal',
    'gradient_blend': 10
}

class InputBox(widgetsBETA.Label):
    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val
        self._show_string = self.show_characters * len(self.string) if self.show_characters not in [None, 0] else self.string

        self._base_text_rendering = pygame.font.SysFont(*self._font_data).render(self._show_string, 1, self.style['foreground'])
        self._base_secondary_text = pygame.font.SysFont(*self._font_data).render(self._show_string, 1, self.style['active_fg'])
        self._text_size = pygame.font.SysFont(*self._font_data).size(self._text)

    def __init__(self, container, style=None, placeholder_text="", font=('gadugi', 15), anchor='topleft', size=(300, 20), padding=(10, 10),
                 multiline=False, show_characters:str=None):
        style = style if style else default_style

        super().__init__(container, style, placeholder_text, font, anchor, size, padding)
        self._base_secondary_rendering = self.render_secondary_hierarchy()
        self._base_secondary_text = pygame.font.SysFont(*font).render(self._text, 1, self.style['active_fg'])
        self._event_mode = 0

        self.multiline = multiline
        self.show_characters = show_characters
        self._scroll_offset = 0
        self._is_hover = False
        self._is_click = False
        self._font_object = pygame.font.SysFont(*self._font_data)
        self._text_size = self._font_object.size(self._text)

        self._active_seperator = pygame.Surface([1, self._text_size[1]])
        self._active_blink_timer = 0

        self._show_string = self.show_characters * len(self.string) if self.show_characters not in [None, 0] else self.string
        self.string = self.string

    def render_secondary_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        size = [x-self.style['borderwidth']*2 for x in self.rect.size]

        padding = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self.style['active_bg'], self.style['cornerradius'],
                                                    orient=self.style['gradial_orient'],
                                                    gradient_blend=self.style['gradient_blend'])
        content = pygame.Surface(self._base_size, pygame.SRCALPHA, 32)
        padding.blit(content, [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        bordercolor = (0, 0, 0, 0) if not self.style['borderwidth'] else self.style['active_bc']

        border = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                   self.style['cornerradius'], orient=self.style['gradial_orient'],
                                                   gradient_blend=self.style['gradient_blend'])

        return [padding, border, content]

    def trigger(self, events, mpos):
        self._is_hover = False
        self._is_click = False
        text_len = pygame.font.SysFont(*self._font_data).size(self._text)[0]

        if self._event_mode:
            self._active_blink_timer += 1
        else:
            self._active_blink_timer = 0

        if self.rect.collidepoint(*mpos):
            self._is_hover = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        elif not any([x._is_hover for x in widgetsBETA.Widget.interactives]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(*event.pos) and event.button == 1:
                    self._is_click = True
                    self._event_mode = not self._event_mode
                else:
                    self._event_mode = False

            if self._event_mode:
                if event.type == pygame.KEYDOWN:
                    self.string = self.string + event.unicode if common.ascii(event.unicode) > 31 else self.string

                    if event.key == pygame.K_BACKSPACE:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10
                        else:
                            self._scroll_offset = 0

                        self.string = self.string[0:-1]

                    elif event.key == pygame.K_DELETE:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10

                        self.string = ''

                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.multiline:
                        self.string += '\n'

                    elif event.key == pygame.K_RIGHT:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10

                        self._scroll_offset = self._scroll_offset - 10 if not text_len < self.rect.width else self._scroll_offset

                    elif event.key == pygame.K_LEFT:
                        self._scroll_offset = min(0, self._scroll_offset+10)

                    elif text_len > self.rect.width:
                        self._scroll_offset = -text_len+self.rect.width-30

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        select_render_list = [self._base_hierarchy_rendering, self._base_secondary_rendering]
        select_render = select_render_list[self._event_mode]

        select_text_list = [self._base_text_rendering, self._base_secondary_text]
        select_text = select_text_list[self._event_mode]

        self._hierarchy_rendering = [select_render[0].copy(),
                                     select_render[1].copy(),
                                     select_render[2].copy()]
        self._text_rendering = select_text.copy()

        text_position = common.anchor_calculation(
            self._hierarchy_rendering[2],
            self._text_rendering,
            self.text_anchor,
            0,
            0
        )

        self._hierarchy_rendering[2].blit(self._text_rendering, [text_position[0]+self._scroll_offset, text_position[1]])

        if self._event_mode and self._active_blink_timer//30 % 2 == 0:
            self._hierarchy_rendering[2].blit(self._active_seperator,
                                              [text_position[0] + self._scroll_offset + self._text_size[0], 0])

        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

