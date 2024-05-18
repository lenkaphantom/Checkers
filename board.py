from typing import Any
import pygame
from constants import *
from piece import Piece

class Board(object):
    def __init__(self):
        self.board = []
        self.brown_left = self.white_left = 12
        self.brown_queens = self.white_queens = 0
        self.create_board()
        
    def __str__(self):
        """
        Funkcija koja vraca string reprezentaciju table.
        """
        string = ""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    string += "0"
                else:
                    if piece.color == BROWN:
                        if piece.queen:
                            string += "B"
                        else:
                            string += "b"
                    else:
                        if piece.queen:
                            string += "W"
                        else:
                            string += "w"
            string += "\n"
        return string

    def draw_squares(self, win):
        """
        Funkcija koja boji polja u BEIGE.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        """
        Funkcija koja postavlja figure na tablu.
        """
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
        """
        Funkcija koja iscrtava tablu na ekran.
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        """
        Funkcija koja pomera figuru u zadati red i kolonu.
        - `piece`: figura koja se pomera
        - `row`: red u koji se pomera
        - `col`: colona u koju se pomera
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == BROWN:
                self.brown_queens += 1
            else:
                self.white_queens += 1

    def get_valid_moves(self, piece):
        """
        Funkcija vraca sve moguce poteze za odredjenu figuru.
        Poziva pomocne funkcije get_moves_left i get_moves_right.
        - `piece`: figura za koju se potezi dobavljaju
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BROWN or piece.queen:
            moves.update(self.get_moves_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.get_moves_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.queen:
            moves.update(self.get_moves_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self.get_moves_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves
    
    def get_moves_left(self, start, stop, step, color, left, captured = []):
        """
        Funkcija dobavlja poteze levo od pocetne figure.
        - `start`: red od kojeg se krece
        - `stop`: krajnji red
        - `step`: korak kojim se krece kroz redove; moze biti +1, kretanje nagore, ili -1, kretanje nadole
        - `color`: boja figure cije poteze dobavljamo
        - `left`: kolona sa leve strane trenutne figure
        - `captured`: lista figura koje se mogu pojedi u toku poteza
        """
        moves = {}
        last = []
        for row in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[row][left]
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(row, left)] = last + captured
                else:
                    moves[(row, left)] = last
                
                if last:
                    if step == -1:
                        new_row = max(row - 3, -1)
                    else:
                        new_row = min(row + 3, ROWS)
                    moves.update(self.get_moves_left(row + step, new_row, step, color, left - 1, captured = last))
                    moves.update(self.get_moves_right(row + step, new_row, step, color, left + 1, captured = last))
                break
            elif current.color == color:
                break
            else:
                last.append(current)

            left -= 1
        
        return moves

    def get_moves_right(self, start, stop, step, color, right, captured = []):
        """
        Funkcija dobavlja poteze desno od pocetne figure.
        - `start`: red od kojeg se krece
        - `stop`: krajnji red
        - `step`: korak kojim se krece kroz redove; moze biti +1, kretanje nagore, ili -1, kretanje nadole
        - `color`: boja figure cije poteze dobavljamo
        - `right`: kolona sa desne strane trenutne figure
        - `captured`: lista figura koje se mogu pojedi u toku poteza
        """
        moves = {}
        last = []
        for row in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[row][right]
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(row, right)] = last + captured
                else:
                    moves[(row, right)] = last
                
                if last:
                    if step == -1:
                        new_row = max(row - 3, -1)
                    else:
                        new_row = min(row + 3, ROWS)
                    moves.update(self.get_moves_left(row + step, new_row, step, color, right - 1, captured = last))
                    moves.update(self.get_moves_right(row + step, new_row, step, color, right + 1, captured = last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def get_pieces_color(self, color):
        """
        Funkcija vraca sve figure zadate boje.
        """
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces
    
    def get_forced_valid_moves(self, color):
        """
        Funkcija vraca sve poteze koje obuhvataju jedenje protivnickih figura ako je moguce pojesti neku figuru.
        - `color`: boja igraca za kojeg se dobavljaju potezi
        """
        pieces = self.get_pieces_color(color)
        moves_by_piece = {}
        temp_moves = {}
        any_captured = False

        for piece in pieces:
            temp_moves = {}
            moves = self.get_valid_moves(piece)
            values = moves.values()
            captured = False
            for value in values:
                if value:
                    captured = True
                    any_captured = True
                    break

            if not any_captured:
                continue
            if any_captured and not captured:
                continue
            
            for move in moves:
                if not moves[move]:
                    continue
                temp_moves[move] = moves[move]
            moves_by_piece[piece] = temp_moves
        if moves_by_piece == {}:
            return False
        return moves_by_piece

    
    def has_valid_moves_for_color(self, color):
        """
        Funkcija koja vraca True ako postoji makar jedan potez za neku figuru zadate boje.
        - `color`: boja za koju se proverava da li ima poteza
        """
        pieces = self.get_pieces_color(color)
        for piece in pieces:
            if self.get_valid_moves(piece):
                return True
        return False
    
    def remove(self, pieces):
        """
        Uklanjanje liste figura sa table.
        - `pieces`: lista figura za uklanjanje
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BROWN:
                    self.brown_left -= 1
                else:
                    self.white_left -= 1

    def count_edge_pieces(self):
        """
        Funkcija koja prebrojava sve figure koje se nalaze na ivicama table.
        Vraca broj belih figura, belih kraljica, braon figura i braon kraljica.
        """
        white_count = 0
        white_count_queens = 0
        
        brown_count = 0
        brown_count_queens = 0

        for row in range(ROWS):
            for col in range(COLS):
                if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
                    piece = self.board[row][col]
                    if piece != 0 and piece.color == WHITE:
                        white_count += 1
                        if piece.queen:
                            white_count_queens += 1
                    elif piece != 0 and piece.color == BROWN:
                        brown_count += 1
                        if piece.queen:
                            brown_count_queens += 1
        return white_count, white_count_queens, brown_count, brown_count_queens

    def evaluate_state(self):
        """
        Heuristicka funkcija zasnovana na broju figura, broju kraljica, broju ivicnih figura i broju ivicnih kraljica.
        """
        white = self.white_left * POINTS['piece'] + self.white_queens * POINTS['queen']
        brown = self.brown_left * POINTS['piece'] + self.brown_queens * POINTS['queen']

        white_edge, white_queen_edge, brown_edge, brown_queen_edge = self.count_edge_pieces()

        white += white_edge * POINTS['side_piece'] + white_queen_edge * POINTS['side_queen']
        brown += brown_edge * POINTS['side_piece'] + brown_queen_edge * POINTS['side_queen']

        return white - brown
    
    def evaluate_end_state(self):
        """
        Heuristicka funkcija koja evaluira finalno stanje table.
        """
        if self.brown_left == 0:
            return float('inf')
        elif self.white_left == 0:
            return float('-inf')
        return 0
    
    def game_over(self, turn):
        """
        Funkcija koja proverava da li je igra zavrsena.
        """
        if self.brown_left <= 0:
            return "WHITE"
        elif self.white_left <= 0:
            return "BROWN"
        if not self.has_valid_moves_for_color(turn):
            if turn == BROWN:
                return "WHITE"
            else:
                return "BROWN"
        return None