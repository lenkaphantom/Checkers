import pygame

from .constants import *
from .piece import Piece
from .board import Board

class Game(object):
    def __init__(self, win, mode):
        self._init()
        self.win = win
        self.mode = mode

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BROWN
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col, mode):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = {}
                self.select(row, col, mode)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            valid_moves_temp = {}
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            values = self.valid_moves.values()
            captured = False
            for value in values: 
                if value:
                    captured = True
                    break
            for move in self.valid_moves:
                if mode == 1 and captured and not self.valid_moves[move]:
                    continue
                valid_moves_temp[move] = self.valid_moves[move]
            self.valid_moves = valid_moves_temp
            return True
        
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self.board.remove(captured)
            self.change_turn()
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves): 
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BROWN:
            self.turn = WHITE
        else:
            self.turn = BROWN
    
    def draw_winner(self):
        self.win.fill(BEIGE)
        winner = self.board.winner()
        font = pygame.font.SysFont(None, 100)
        text = font.render(f"{winner} Wins!", True, BROWN)
        self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
        pygame.display.update()