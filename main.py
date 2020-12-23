import pygame
from config import *
import config
from drawing import Drawing
from figure import Figure


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris')
    screen = pygame.display.set_mode(SIZE)

    drawing = Drawing(screen)
    current_figure = Figure()
    other = []

    clock = pygame.time.Clock()

    running = True
    state = 1
    falling = 0
    deleted_row = None

    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = 1
                    score = 0
                    config.BOARD = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
                    current_figure = Figure()
                    other = []
                elif event.key == pygame.K_s:
                    config.TIME_BY_CELL = int(config.TIME_BY_CELL / 3)
                else:
                    if state == 1:
                        current_figure.change(event.key)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    config.TIME_BY_CELL = int(config.TIME_BY_CELL * 3)

        if state == 1:
            current_figure, previous_figure = current_figure.update()
            if falling > 0:
                other = [i.update(forcibly=(i.positions[0][1] <= deleted_row)) for i in other]
                for i in range(len(other)):
                    other[i] = other[i][0] if not other[i][1] else other[i][1]
                falling -= 1
            if not current_figure:
                for i in previous_figure.positions:
                    config.BOARD[i[1]][i[0]] = previous_figure.color
                    other.append(Figure([i], previous_figure.color))

                destroyed_lines = 0
                for i in range(BOARD_HEIGHT):
                    if 0 not in config.BOARD[i]:
                        destroyed_lines += 1
                        for k in range(i, 0, -1):
                            config.BOARD[k] = config.BOARD[k - 1][:]
                        deleted_row = i
                        falling += TIME_BY_CELL
                        other = [j for j in other if j.positions[0][1] != i]
                score += 2 ** destroyed_lines if destroyed_lines else 0

                current_figure = Figure()
                if len(set(config.BOARD[0])) != 1:
                    state = 0
                    continue

            screen.fill(BACKGROUND)
            drawing.board()
            drawing.figure(current_figure)
            # for i in other:
            #     drawing.figure(i)
            drawing.score(score)
            drawing.info()
        elif state == 0:
            drawing.lose()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
