from interface import Element, Image, Text
from core import Figure, Base
from config import *
import config


class Field(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.img_field = Image({
            'position': (0, 0),
            'path': 'static/field',
        })
        self.img_next = Image({
            'position': (300, 77),
            'path': 'static/next',
        })
        self.img_hold = Image({
            'position': (450, 77),
            'path': 'static/hold',
        })
        self.txt_score = Text({
            'position': (300, 300),
            'text': 'Score: 0',
        })
        self.current = pygame.Surface((BOARD_SIZE[0] * TILE,
                                       BOARD_SIZE[1] * TILE))
        self.base = Base()
        self.figure = Figure()
        self.next = Figure()
        self.hold = None
        self.hold_first = True
        self.score = 0
        self.state = '__WAIT__'
        self.field = [[0 for _ in range(BOARD_SIZE[0])]
                      for _ in range(BOARD_SIZE[1])]

    def get(self, position, shift=(0, 0)):
        if all([
            0 <= position[1] + shift[1] < BOARD_SIZE[1],
            0 <= position[0] + shift[0] < BOARD_SIZE[0],
        ]):
            return self.field[position[1] + shift[1]][position[0] + shift[0]]
        return 1

    def set(self, position, value):
        self.field[position[1]][position[0]] = value

    def start(self):
        self.base = Base()
        self.figure = Figure()
        self.next = Figure()
        self.hold = None
        self.score = 0
        self.txt_score.set_text('Score: 0')
        self.state = '__GAME__'
        self.field = [[0 for _ in range(BOARD_SIZE[0])]
                      for _ in range(BOARD_SIZE[1])]

    def key_down(self, key):
        if key == pygame.K_a:
            if self.figure.can_move(self, (-1, 0)):
                self.figure.move((-1, 0))
        elif key == pygame.K_d:
            if self.figure.can_move(self, (1, 0)):
                self.figure.move((1, 0))
        elif key == pygame.K_q:
            if self.figure.can_rotate(self, 3):
                self.figure.rotate(3)
        elif key == pygame.K_e:
            if self.figure.can_rotate(self, 1):
                self.figure.rotate(1)
        elif key == pygame.K_w:
            if not self.hold:
                if self.hold_first:
                    self.hold = self.figure.copy()
                    self.figure = Figure()
                    self.hold_first = False
            else:
                self.figure = self.hold.copy()
                self.hold = None
        elif key == pygame.K_n:
            self.start()

    def show(self, surf):
        if self.state == '__GAME__':
            if self.figure.state == '__STOP__':
                if self.figure.can_move(self, (0, 1)):
                    self.figure.state = '__FALLING__'
                else:
                    self.hold_first = True
                    for block in self.figure.blocks:
                        self.set(block.position, 1)
                    deleted = []
                    self.base.add_blocks(self.figure)
                    for i in range(len(self.field)):
                        if all([self.get((k, i))
                                for k in range(len(self.field[i]))]):
                            for row in range(i, 0, -1):
                                self.field[row] = self.field[row - 1]
                            deleted.append(i)
                            self.field[0] = [0 for _ in range(BOARD_SIZE[0])]
                    self.base.set_deleted(deleted)
                    if any([i == 1 for i in self.field[0]]):
                        self.state = '__LOSE__'
                        config.UPDATER.send_result(self.score)
                        if config.NICKNAME:
                            rating = config.WINDOW.get('txtRating')
                            rating.set_text(int(rating.text) + self.score)
                            best = config.WINDOW.get('txtBest')
                            best.set_text(max(int(best.text), self.score))
                    self.score += 2 ** len(deleted) if deleted else 0
                    self.txt_score.set_text('Score: ' + str(self.score))
                    self.figure = self.next
                    self.next = Figure()
        self.current.fill(BACKGROUND)
        self.img_field.show(self.current)
        if self.state == '__GAME__':
            self.figure.show(self.current)
        self.base.show(self.current)
        self.img_next.show(surf)
        self.img_hold.show(surf)
        if self.hold and self.state == '__GAME__':
            self.hold.static_show(surf, self.img_hold)
        if self.state == '__GAME__':
            self.next.static_show(surf, self.img_next)
        self.txt_score.show(surf)
        surf.blit(self.current, self.position)
