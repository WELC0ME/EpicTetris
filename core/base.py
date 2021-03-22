from config import *


class Base:

    def __init__(self):
        self.blocks = []
        self.mask = []
        self.state = '__WAIT__'
        self.shift = 0

    def add_blocks(self, figure):
        self.blocks.extend(figure.blocks)
        self.mask.extend([0 for _ in range(len(figure.blocks))])

    def set_deleted(self, rows):
        new_blocks = []
        new_mask = []
        for block in self.blocks:
            if block.position[1] not in rows:
                new_blocks.append(block)
                new_mask.append(len([1 for row in rows
                                    if block.position[1] < row]))
        self.state = '__FALLING__'
        self.blocks = new_blocks
        self.mask = new_mask

    def show(self, surf):
        for i, block in enumerate(self.blocks):
            block.show(surf, shift=self.shift if self.mask[i] > 0 else 0)

        if self.state == '__FALLING__':
            self.shift += FALLING_SPEED
        if self.shift >= TILE:
            for i, block in enumerate(self.blocks):
                if self.mask[i] > 0:
                    block.position = (block.position[0], block.position[1] + 1)
                    self.mask[i] -= 1
            self.shift = 0
            if all([i == 0 for i in self.mask]):
                self.state = '__STOP__'
