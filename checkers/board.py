import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, BEIGE, BLACK

class Board(object):
    def __intit__(self):
        self._board = []
        self._turn = 0
        self._selected_piece = None
        self._brown_left = self._white_left = 12
        self._brown_queens = self._white_queens = 0

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    