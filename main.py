import time
import subprocess
from config import *
from interface import *
from core import Field
import updater
import config

if __name__ == '__main__':
    config.CLIENT = subprocess.Popen([sys.executable, 'client.py'])
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Epic Tetris')
    pygame.event.set_allowed([
        pygame.QUIT,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEMOTION,
        pygame.KEYDOWN,
    ])

    config.FONT = pygame.font.Font(None, 40)
    config.WINDOW = eval(open(gsp('interface.interface'), 'r',
                              encoding='utf8').read())
    config.UPDATER = updater.Updater()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                config.WINDOW.mouse_down(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                config.WINDOW.mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                config.WINDOW.key_down(event.key)
        config.UPDATER.update()
        screen.fill(BACKGROUND)
        config.WINDOW.show(screen)
        pygame.display.flip()
        time.sleep(1 / FPS)
