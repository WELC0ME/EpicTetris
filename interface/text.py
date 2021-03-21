from interface import Element
import config


class Text(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.image = None
        self.text = ''
        self.hidden = settings.get('hidden', False)
        self.set_text(settings.get('text', ''))

    def set_text(self, text):
        self.text = str(text)
        if self.hidden:
            text = '*' * len(str(text))
        self.image = config.FONT.render(str(text), True, config.TEXT)

    def show(self, surf):
        surf.blit(self.image, self.position)
