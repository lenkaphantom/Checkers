import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, BEIGE, BLACK, WHITE, BROWN
from .piece import Piece

class Board(object):
    def __init__(self):
        self.board = []
        self.turn = 0
        self.brown_left = self.white_left = 12
        self.brown_queens = self.white_queens = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BROWN))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == BROWN:
                self.brown_queens += 1
            else:
                self.white_queens += 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BROWN or piece.queen:
            moves.update(self._get_moves_to_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._get_moves_to_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.queen:
            moves.update(self._get_moves_to_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._get_moves_to_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves
    
    def _get_moves_to_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[row][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, left)] = last + skipped
                else:
                    moves[(row, left)] = last
                
                if last:
                    if step == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, ROWS)
                    moves.update(self._get_moves_to_left(row + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._get_moves_to_right(row + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            left -= 1
        
        return moves
    
    def _get_moves_to_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[row][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, right)] = last + skipped
                else:
                    moves[(row, right)] = last
                
                if last:
                    if step == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, ROWS)
                    moves.update(self._get_moves_to_left(row + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._get_moves_to_(row + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            right += 1
        
        return moves