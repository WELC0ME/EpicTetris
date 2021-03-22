import random
from config import *
from core import Block


class Figure:

    def __init__(self, color=None, options=None):
        self.color = color if color else random.randint(0, 7)
        self.options = options if options else random.choice(FIGURES)
        self.rotation = 0
        self.state = '__STOP__'
        self.blocks = []
        self.shift = 0
        self.corner = (BOARD_SIZE[0] // 2, 0)
        for i, v in enumerate(self.options[self.rotation]):
            x, y = i % 4, i // 4
            if v == '1':
                self.blocks.append(Block(self.color, (self.corner[0] + x,
                                                      self.corner[1] + y)))

    def copy(self):
        return Figure(self.color, self.options)

    def show(self, surf):
        [i.show(surf, shift=self.shift) for i in self.blocks]
        if self.state == '__FALLING__':
            self.shift += FALLING_SPEED
        if self.shift >= TILE:
            for block in self.blocks:
                block.position = (block.position[0], block.position[1] + 1)
            self.corner = (self.corner[0], self.corner[1] + 1)
            self.shift = 0
            self.state = '__STOP__'

    def static_show(self, surf, image):
        pos = (image.position[0] + 25, image.position[1] + 45)
        for i, v in enumerate(self.options[self.rotation]):
            x, y = i % 4, i // 4
            if v == '1':
                tmp_block = Block(self.color, (0, 0))
                surf.blit(tmp_block.image, (pos[0] + x * TILE,
                                            pos[1] + y * TILE))

    def can_move(self, field, direction):
        check = all([field.get(block.position, direction) == 0
                     for block in self.blocks])
        if self.state == '__FALLING__':
            direction = (direction[0], direction[1] + 1)
            check = (check and all([field.get(block.position, direction) == 0
                                    for block in self.blocks]))
        return check

    def move(self, direction):
        self.corner = (self.corner[0] + direction[0],
                       self.corner[1] + direction[1])
        for block in self.blocks:
            block.position = (block.position[0] + direction[0],
                              block.position[1] + direction[1])

    def can_rotate(self, field, turnover):
        rotation = (self.rotation + turnover) % 4
        new_blocks = []
        for i, v in enumerate(self.options[rotation]):
            x, y = i % 4, i // 4
            if v == '1':
                new_blocks.append(Block(self.color, (self.corner[0] + x,
                                                     self.corner[1] + y)))
        check = all([field.get(block.position) == 0 for block in new_blocks])
        if self.state == '__FALLING__':
            check = (check and all([field.get(block.position, (0, 1)) == 0
                                    for block in new_blocks]))
        return check

    def rotate(self, turnover):
        self.rotation = (self.rotation + turnover) % 4
        self.blocks = []
        for i, v in enumerate(self.options[self.rotation]):
            x, y = i % 4, i // 4
            if v == '1':
                self.blocks.append(Block(self.color, (self.corner[0] + x,
                                                      self.corner[1] + y)))
