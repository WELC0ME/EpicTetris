from interface import Element, Text


class TextArea(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.elements = {
            'number': Text({
                'position': (self.position[0] + 0, self.position[1]),
                'text': '',
            }),
            'nickname': Text({
                'position': (self.position[0] + 30, self.position[1]),
                'text': '',
            }),
            'rating': Text({
                'position': (self.position[0] + 210, self.position[1]),
                'text': '',
            }),
            'best': Text({
                'position': (self.position[0] + 320, self.position[1]),
                'text': '',
            }),
            'created': Text({
                'position': (self.position[0] + 400, self.position[1]),
                'text': '',
            }),
        }
        if 'user' in settings.keys():
            self.set_text(settings['user'])

    def set_text(self, user):
        for i in list(user.keys()):
            if i in list(self.elements.keys()):
                self.elements[i].set_text(user[i])

    def show(self, surf):
        [i.show(surf) for i in list(self.elements.values())]
