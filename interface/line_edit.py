import pygame
from interface import Element, Text, Button


class LineEdit(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.content = Text({
            'position': (self.position[0] + 20, self.position[1] + 15),
            'text': '',
            'hidden': settings.get('hidden', False)
        })
        self.base = Button({
            'position': self.position,
            'path': 'line_edit',
            'function': 'line_edit',
            'args': '["' + settings['name'] + '"]',
        })
        self.name = settings['name']

    def mouse_motion(self, pos):
        self.base.mouse_motion(pos)

    def mouse_down(self, pos):
        self.base.mouse_down(pos)

    def key_down(self, key):
        if self.base.animation != 'pressed':
            return
        letter = pygame.key.name(key)
        if letter == 'backspace':
            self.content.set_text(self.content.text[:-1])
        elif len(letter) == 1 and len(self.content.text) < 10:
            self.content.set_text(self.content.text + letter)

    def show(self, surf):
        self.base.show(surf)
        self.content.show(surf)
