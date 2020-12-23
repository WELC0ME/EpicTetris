SIZE = WIDTH, HEIGHT = 600, 600
FPS = 60
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
TILE = 21
xShift, yShift = (WIDTH - BOARD_WIDTH * TILE) // 4, (HEIGHT - BOARD_HEIGHT * TILE) // 2
START_POSITION = BOARD_WIDTH // 2, 0
SCORE_POSITION = xShift + BOARD_WIDTH * TILE + 30, yShift
LOSE_POSITION = xShift + BOARD_WIDTH * TILE + 30, yShift + 100
RESTART_POSITION = xShift + BOARD_WIDTH * TILE + 30, yShift + 200
SCOREBOARD_POSITION = xShift + BOARD_WIDTH * TILE + 30, yShift + 300
INFO_COLOR = (200, 70, 70)
COLORS_NUMBER = 7
FALLING_SPEED = 1
TIME_BY_CELL = 15
MOVE_SPEED = 1
BACKGROUND = (0, 0, 0)

FIGURES_R0 = [[(0, 0), (1, 0), (2, 0), (3, 0)],
              [(0, 0), (1, 0), (0, 1), (1, 1)],
              [(0, 0), (1, 0), (2, 0), (1, 1)],
              [(0, 0), (1, 0), (2, 0), (0, 1)],
              [(0, 0), (1, 0), (2, 0), (2, 1)],
              [(0, 0), (1, 0), (1, 1), (2, 1)],
              [(0, 1), (1, 1), (1, 0), (2, 0)]]

FIGURES_R1 = [[(0, 0), (-1, 1), (-2, 2), (-3, 3)],
              [(0, 0), (0, 0), (0, 0), (0, 0)],
              [(0, 1), (0, 0), (-1, 1), (0, 1)],
              [(0, 0), (0, 0), (-1, 1), (1, 1)],
              [(0, 2), (0, 0), (-1, 1), (-1, 1)],
              [(0, 1), (0, 0), (0, 0), (-2, 1)],
              [(0, 0), (0, 0), (-1, 0), (-1, 2)]]

FIGURES_R2 = [[(0, 0), (1, -1), (2, -2), (3, -3)],
              [(0, 0), (0, 0), (0, 0), (0, 0)],
              [(0, 0), (0, 0), (0, 0), (1, -1)],
              [(0, 1), (0, 1), (1, 0), (1, -2)],
              [(0, -2), (-1, 1), (0, 0), (1, -1)],
              [(0, -1), (0, 0), (0, 0), (2, -1)],
              [(0, 0), (0, 0), (1, 0), (1, -2)]]

FIGURES_R3 = [[(0, 0), (-1, 1), (-2, 2), (-3, 3)],
              [(0, 0), (0, 0), (0, 0), (0, 0)],
              [(0, -1), (-1, 1), (0, 0), (-2, 1)],
              [(0, -1), (-1, 0), (-2, 1), (-1, 2)],
              [(0, 0), (1, -1), (-1, 0), (-2, 1)],
              [(0, 1), (0, 0), (0, 0), (-2, 1)],
              [(0, 0), (0, 0), (-1, 0), (-1, 2)]]

FIGURES_R4 = [[(0, 0), (1, -1), (2, -2), (3, -3)],
              [(0, 0), (0, 0), (0, 0), (0, 0)],
              [(0, 0), (1, -1), (1, -1), (1, -1)],
              [(0, 0), (1, -1), (2, -2), (-1, -1)],
              [(0, 0), (0, 0), (2, -1), (2, -1)],
              [(0, -1), (0, 0), (0, 0), (2, -1)],
              [(0, 0), (0, 0), (1, 0), (1, -2)]]

FIGURES_ROTATE = [FIGURES_R1, FIGURES_R2, FIGURES_R3, FIGURES_R4]
FIGURES_NUMBER = len(FIGURES_R0)
BOARD = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
