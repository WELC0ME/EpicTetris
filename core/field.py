from interface import Element, Image, Text
from core import Figure
from config import *
import config


class Field(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.field = [[0 for _ in range(BOARD_SIZE[0])]
                      for _ in range(BOARD_SIZE[1])]
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

        self.block = None
        self.other = []
        self.falling = 0
        self.deleted_row = None
        self.score = 0
        self.keys = {i: ldi(gip('blocks/' + str(i) + '.png'))
                     for i in range(9)}
        self.state = '__WAIT__'

    def start(self):
        self.field = [[0 for _ in range(BOARD_SIZE[0])]
                      for _ in range(BOARD_SIZE[1])]
        self.block = Figure(self)
        self.other = []
        self.falling = 0
        self.deleted_row = None
        self.score = 0
        self.state = '__GAME__'

    def key_down(self, key):
        if self.state == '__GAME__':
            self.block.change(key)

    def show(self, surf):
        if self.state == '__GAME__':
            self.block, previous = self.block.update()
            if self.falling > 0:
                self.other = [i.update(forcibly=(
                        i.positions[0][1] <= self.deleted_row))
                    for i in self.other]
                for i in range(len(self.other)):
                    if not self.other[i][1]:
                        self.other[i] = self.other[i][0]
                    else:
                        self.other[i] = self.other[i][1]
                self.falling -= 1
            if not self.block:
                for i in previous.positions:
                    self.field[i[1]][i[0]] = previous.color
                    self.other.append(Figure([i], previous.color))

                destroyed_lines = 0
                for i in range(BOARD_SIZE[1]):
                    if 0 not in self.field[i]:
                        destroyed_lines += 1
                        for k in range(i, 0, -1):
                            self.field[k] = self.field[k - 1][:]
                        self.deleted_row = i
                        self.falling += TIME_BY_CELL
                        print(self.other)
                        print([j.positions for j in self.other])
                        self.other = [j for j in self.other
                                      if j.positions[0][1] != i]
                self.score += 2 ** destroyed_lines if destroyed_lines else 0
                self.txt_score.set_text('Score:' + str(self.score))
                self.block = Figure(self)
                if len(set(self.field[0])) != 1:
                    config.UPDATER.send_result(self.score)
                    self.state = '__LOSE__'

        self.current.fill(BACKGROUND)

        for i in range(BOARD_SIZE[1]):
            for k in range(BOARD_SIZE[0]):
                self.current.blit(self.keys[0],
                                  (k * TILE, i * TILE))
                self.current.blit(self.keys[self.field[i][k]],
                                  (k * TILE, i * TILE))
        if self.block:
            for i in range(len(self.block.positions)):
                self.current.blit(self.keys[self.block.color],
                                  (self.block.positions[i][0] * TILE,
                                   self.block.positions[i][1] * TILE))

        self.img_next.show(surf)
        self.img_hold.show(surf)
        self.txt_score.show(surf)
        surf.blit(self.current, self.position)
