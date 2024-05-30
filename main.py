import pygame
from constants import *
from game import Game
from algorithm import alpha_beta_pruning

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_mode_selection_menu():
    run_menu = True
    font = pygame.font.SysFont(None, 40)
    while run_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(BROWN)

        text = font.render("Choose Game Mode:", True, WHITE)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))

        button_width = 500
        button_height = 60
        button_gap = 40

        button_y1 = HEIGHT // 2 - button_height // 2 - button_gap // 2
        button_y2 = HEIGHT // 2 + button_height // 2 + button_gap // 2

        button_rect1 = pygame.Rect(WIDTH // 2 - button_width // 2, button_y1, button_width, button_height)
        button_rect2 = pygame.Rect(WIDTH // 2 - button_width // 2, button_y2, button_width, button_height)

        pygame.draw.rect(WIN, BEIGE, button_rect1)
        pygame.draw.rect(WIN, BEIGE, button_rect2)

        text = font.render("With Forced Capturing", True, BROWN)
        text_rect = text.get_rect(center=button_rect1.center)
        WIN.blit(text, text_rect)

        text = font.render("Without Forced Capturing", True, BROWN)
        text_rect = text.get_rect(center=button_rect2.center)
        WIN.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if button_rect1.collidepoint(mouse_pos):
                return 1
            elif button_rect2.collidepoint(mouse_pos):
                return 0

        pygame.display.update()


def main():
    pygame.init()
    mode = display_mode_selection_menu()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN, mode)

    while run:
        clock.tick(FPS)

        if game.board.game_over(game.turn) is not None:
            pygame.time.delay(900)
            game.draw_winner()
            pygame.time.delay(2500)
            run = False

        if game.turn == WHITE:
            best_move, moved_piece = alpha_beta_pruning(game.board, 7, game.turn, mode)
            game.ai_move(best_move, moved_piece)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                game.select(row, col, mode)
        game.update()
    pygame.quit()

if __name__ == '__main__':
    main()