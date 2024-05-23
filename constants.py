import pygame

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
PADDING = 13
BORDER = 2

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
    'queen': 50,
    'middle_piece': 10,
    'promotion': 20,
    'safe': 10,
    'defend': 10,
    'jump': 15,
    'special_defend': 20,
    'special_jump': 20
}