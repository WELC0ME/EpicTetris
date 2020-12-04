import random
import pygame
from config import *
import config


class Figure:

    def __init__(self, positions=None, color=None):
        random.seed()
        self.figure_number = random.randint(0, FIGURES_NUMBER - 1)
        self.rotate_counter = 0
        if not positions:
            self.positions = [(START_POSITION[0] + i[0],
                               START_POSITION[1] + i[1]) for i in FIGURES_R0[self.figure_number]]
            self.color = random.randint(1, COLORS_NUMBER)
        else:
            self.positions = positions
            self.color = color
        self.falling_counter = 0

    def update(self, forcibly=False):

        if self.falling_counter == 0:
            for i in range(len(self.positions)):
                if not self.check_position(self.positions[i][0],
                                           self.positions[i][1] + FALLING_SPEED, forcibly=forcibly):
                    if forcibly:
                        self.falling_counter = -config.TIME_BY_CELL
                        return self, False
                    return False, self
        if self.falling_counter > 0:
            for i in range(len(self.positions)):
                self.positions[i] = (self.positions[i][0],
                                     self.positions[i][1] + FALLING_SPEED / config.TIME_BY_CELL)

        self.falling_counter += 1
        if self.falling_counter >= config.TIME_BY_CELL:
            for i in range(len(self.positions)):
                self.positions[i] = (self.positions[i][0], int(round(self.positions[i][1])))
            self.falling_counter = 0

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
            if not self.check_position(self.positions[i][0] + direction, int(self.positions[i][1])):
                return
            if self.falling_counter != 0:
                if not self.check_position(self.positions[i][0] + direction, int(self.positions[i][1]) + 1):
                    return
        for i in range(len(self.positions)):
            self.positions[i] = (self.positions[i][0] + direction, self.positions[i][1])

    def rotate(self, adj):

        for k in range(adj):
            ROTATED = FIGURES_ROTATE[self.rotate_counter]
            for i in range(len(self.positions)):
                newX = self.positions[i][0] + ROTATED[self.figure_number][i][0]
                newY = int(self.positions[i][1] + FALLING_SPEED) + ROTATED[self.figure_number][i][1]
                if not self.check_position(newX, newY):
                    return
            for i in range(len(self.positions)):
                newX = self.positions[i][0] + ROTATED[self.figure_number][i][0]
                newY = self.positions[i][1] + ROTATED[self.figure_number][i][1]
                self.positions[i] = (newX, newY)
            self.rotate_counter = (self.rotate_counter + 1) % 4

    @staticmethod
    def check_position(x, y, forcibly=False):
        return 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT and (forcibly or config.BOARD[y][x] == 0)
