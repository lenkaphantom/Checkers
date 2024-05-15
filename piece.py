import pygame
from constants import *

class Piece(object):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """
        Funkcija koja racuna poziciju figure na tabli.
        """
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def make_queen(self):
        self.queen = True

    def draw(self, win):
        """
        Funkcija koja iscrtava figuru na ekran.
        """
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + BORDER)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.queen:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Funkcija koja pomera u novu vrstu i kolonu.
        - `row` - nova vrsta figure
        - `col` - nova kolona figure
        """
        self.row = row
        self.col = col
        self.calculate_position()