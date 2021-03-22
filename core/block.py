from config import *


class Block:

    def __init__(self, color, position):
        self.position = position
        self.image = ldi(gip('blocks/' + str(color) + '.png'))

    def show(self, surf, shift=0):
        surf.blit(self.image, (self.position[0] * TILE,
                               self.position[1] * TILE + shift))
