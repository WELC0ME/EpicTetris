import pygame
from config import *
import config


class Drawing:

    def __init__(self, surf):
        self.surf = surf
        self.keys = {0: pygame.image.load('Sprites/empty.jpg'),
                     1: pygame.image.load('Sprites/red.jpg'),
                     2: pygame.image.load('Sprites/blue.jpg'),
                     3: pygame.image.load('Sprites/dark_blue.jpg'),
                     4: pygame.image.load('Sprites/yellow.jpg'),
                     5: pygame.image.load('Sprites/green.jpg'),
                     6: pygame.image.load('Sprites/purple.jpg'),
                     7: pygame.image.load('Sprites/orange.jpg')}

    def board(self):
        for i in range(BOARD_HEIGHT):
            for k in range(BOARD_WIDTH):
                self.surf.blit(self.keys[config.BOARD[i][k]], (xShift + k * TILE, yShift + i * TILE))

    def figure(self, figure):
        for i in range(len(figure.positions)):
            self.surf.blit(self.keys[figure.color], (xShift + figure.positions[i][0] * TILE,
                                                     yShift + figure.positions[i][1] * TILE))

    def score(self, value):
        self.surf.blit(pygame.font.Font(None, 50).render("Score: " + str(value), True, INFO_COLOR), SCORE_POSITION)

    def lose(self):
        self.surf.blit(pygame.font.Font(None, 50).render("You lose!", True, INFO_COLOR), LOSE_POSITION)
        self.surf.blit(pygame.font.Font(None, 50).render("'R' - restart", True, INFO_COLOR), RESTART_POSITION)
