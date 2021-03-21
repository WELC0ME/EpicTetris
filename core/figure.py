import random
from config import *


class Figure:

    def __init__(self, field, positions=None, color=None):
        random.seed()
        self.number = random.randint(0, len(FIGURES_R0) - 1)
        self.rotation = 0
        if not positions:
            self.positions = [(BOARD_SIZE[0] // 2 + i[0], i[1])
                              for i in FIGURES_R0[self.number]]
            self.color = random.randint(1, 8)
        else:
            self.positions = positions
            self.color = color
        self.falling = 0
        self.field = field

    def update(self, forcibly=False):

        if self.falling == 0:
            for i in range(len(self.positions)):
                if not self.check_position(self.positions[i][0],
                                           self.positions[i][1] + 1,
                                           forcibly=forcibly):
                    if forcibly:
                        self.falling = -TIME_BY_CELL
                        return self, False
                    return False, self
        if self.falling > 0:
            for i in range(len(self.positions)):
                self.positions[i] = (
                    self.positions[i][0],
                    self.positions[i][1] + 1 / TIME_BY_CELL)

        self.falling += 1
        if self.falling >= TIME_BY_CELL:
            for i in range(len(self.positions)):
                self.positions[i] = (self.positions[i][0],
                                     int(round(self.positions[i][1])))
            self.falling = 0

        return self, False

    def change(self, button):
        keys = {pygame.K_a: [self.move, -1],
                pygame.K_d: [self.move, 1],
                pygame.K_e: [self.rotate, 1],
                pygame.K_q: [self.rotate, 3]}
        if button not in keys.keys():
            return
        keys[button][0](keys[button][1])

    def move(self, direction):
        for i in range(len(self.positions)):
            if not self.check_position(self.positions[i][0] + direction,
                                       int(self.positions[i][1])):
                return
            if self.falling != 0:
                if not self.check_position(self.positions[i][0] + direction,
                                           int(self.positions[i][1]) + 1):
                    return
        for i in range(len(self.positions)):
            self.positions[i] = (self.positions[i][0] + direction,
                                 self.positions[i][1])

    def rotate(self, adj):

        for k in range(adj):
            rotated = FIGURES_ROTATE[self.rotation]
            for i in range(len(self.positions)):
                new_x = self.positions[i][0] + rotated[self.number][i][0]
                new_y = int(self.positions[i][1] + 1)
                new_y += rotated[self.number][i][1]
                if not self.check_position(new_x, new_y):
                    return
            for i in range(len(self.positions)):
                new_x = self.positions[i][0] + rotated[self.number][i][0]
                new_y = self.positions[i][1] + rotated[self.number][i][1]
                self.positions[i] = (new_x, new_y)
            self.rotation = (self.rotation + 1) % 4

    def check_position(self, x, y, forcibly=False):
        return all([
            0 <= x < BOARD_SIZE[0],
            0 <= y < BOARD_SIZE[1],
        ]) and (forcibly or self.field.field[y][x] == 0)
