import pygame
import sys

SIZE = (600, 600)
FPS = 60

WINDOW = None
ACTIVE_LINE_EDIT = ''
FONT = None

# Game
BOARD_SIZE = (10, 25)
TILE = 20
FALLING_SPEED = 5
FIGURES = [
    ['1000100010001000', '1111000000000000', '1000100010001000', '1111000000000000'],
    ['1100110000000000', '1100110000000000', '1100110000000000', '1100110000000000'],
    ['1110010000000000', '0100110001000000', '0100111000000000', '1000110010000000'],
    ['1110100000000000', '1100010001000000', '0010111000000000', '1000100011000000'],
    ['1110001000000000', '0100010011000000', '1000111000000000', '1100100010000000'],
    ['1100011000000000', '0100110010000000', '1100011000000000', '0100110010000000'],
    ['0110110000000000', '1000110001000000', '0110110000000000', '1000110001000000'],
]

# network
SERVER = 'http://epic-tetris-server.herokuapp.com/api/users'
NICKNAME = ''
CLIENT = None
UPDATER = None

# Colors
BACKGROUND = (34, 40, 49)
TEXT = (222, 222, 222)
BLACK = (0, 0, 0)

# Functions
gsp = lambda _p: 'data/' + _p
gip = lambda _p: gsp('images/' + _p)
gap = lambda _p: gsp('audio/' + _p)
gdp = lambda _p: gsp('database/' + _p)
ldi = lambda _p: pygame.image.load(_p)


def shutdown():
    pygame.quit()
    CLIENT.kill()
    sys.exit()
