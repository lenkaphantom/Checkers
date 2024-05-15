import pygame

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (159, 129, 112)
BLUE = (0, 0, 220)
BEIGE = (225, 225, 210)
GREY = (128, 128, 128)

CROWN = pygame.image.load('crown.png')
CROWN = pygame.transform.scale(CROWN, (44, 25))

POINTS = {
    'piece': 1,
    'queen': 5,
    'side_piece': 2,
    'side_queen': 10
}