from interface import Image
import config


class Button(Image):

    def __init__(self, settings):
        settings['path'] = 'buttons/' + settings['path']
        super().__init__(settings)
        self.size = self.images[self.animation].get_rect().size
        self.function = settings['function']
        self.args = settings.get('args', "[]")

    def collide(self, pos):
        return all([
            self.position[0] <= pos[0],
            pos[0] <= self.position[0] + self.size[0],
            self.position[1] <= pos[1],
            pos[1] <= self.position[1] + self.size[1],
        ])

    def mouse_down(self, pos):
        if self.collide(pos):
            eval(self.function)(*eval(self.args))

    def mouse_motion(self, pos):
        if self.collide(pos):
            if self.animation == 'idle':
                self.animation = 'hover'
        else:
            if self.animation == 'hover':
                self.animation = 'idle'


def change_tab(name):
    config.WINDOW.change_tab(name)


def sign_in():
    config.UPDATER.sign_in()


def sign_up():
    config.UPDATER.sign_up()


def get_users():
    config.UPDATER.get_users()


def line_edit(name):
    config.ACTIVE_LINE_EDIT = name


def new_game():
    config.WINDOW.get('fldField').start()
