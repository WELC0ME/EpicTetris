import pygame
from config import *
from network import Network
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
        self.network = Network()

    def board(self):
        for i in range(BOARD_HEIGHT):
            for k in range(BOARD_WIDTH):
                self.surf.blit(self.keys[config.BOARD[i][k]], (xShift + k * TILE, yShift + i * TILE))

    def figure(self, figure):
        for i in range(len(figure.positions)):
            self.surf.blit(self.keys[figure.color], (xShift + figure.positions[i][0] * TILE,
                                                     yShift + figure.positions[i][1] * TILE))

    def score(self, value):
        self.surf.blit(pygame.font.Font(None, 50).render("Score: " + str(value), True, INFO_COLOR), ROW)

    def info(self):
        self.surf.blit(pygame.font.Font(None, 50).render("'R' - restart", True, INFO_COLOR), get_row(1))
        self.surf.blit(pygame.font.Font(None, 50).render("'B' - scoreboard", True, INFO_COLOR), get_row(2))

    def lose(self):
        self.surf.blit(pygame.font.Font(None, 50).render("You lose!", True, INFO_COLOR), get_row(1))
        self.surf.blit(pygame.font.Font(None, 50).render("'V' - save", True, INFO_COLOR), get_row(2))
        self.surf.blit(pygame.font.Font(None, 50).render("'R' - restart", True, INFO_COLOR), get_row(3))
        self.surf.blit(pygame.font.Font(None, 50).render("'B' - scoreboard", True, INFO_COLOR), get_row(4))

    def scoreboard(self):
        step = 40
        res = self.network.get()
        try:
            if not res:
                raise IndexError
            data = {i.split('_')[0]: int(i.split('_')[1]) for i in res.split('\\n')[:-1]}
            out = []
            maximums = sorted(list(set([data[j] for j in data.keys()])), reverse=True)
            counter = 0
            while True:
                if counter >= len(maximums):
                    break
                mx = maximums[counter]
                counter += 1
                for k in data.keys():
                    if data[k] == mx:
                        out.append((k, data[k]))
                        if len(out) == 10:
                            break
                if len(out) == 10:
                    break
            for i in range(len(out)):
                self.surf.blit(pygame.font.Font(None, 30).render(str(out[i]), True, INFO_COLOR), (xShift, yShift + step * i))
        except IndexError:
            print('Something went wrong')

        self.surf.blit(pygame.font.Font(None, 30).render('Press Q to exit', True, INFO_COLOR), (xShift, yShift + step * 10))

    def saving(self, name, score):
        self.surf.blit(pygame.font.Font(None, 30).render('You name ' + name, True, INFO_COLOR),
                       (xShift, yShift))
        self.surf.blit(pygame.font.Font(None, 30).render('You score ' + str(score), True, INFO_COLOR),
                       (xShift, yShift + 100))
        self.surf.blit(pygame.font.Font(None, 30).render('Press H to save', True, INFO_COLOR),
                       (xShift, yShift + 200))
        self.surf.blit(pygame.font.Font(None, 30).render('Press Q to exit', True, INFO_COLOR),
                       (xShift, yShift + 300))

    def send(self, name, score):
        self.network.send(str(name) + '_' + str(score))

    def clear(self):
        self.network.clear()
