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
        Koristi pomocnu funkciju get_moves.
        - `piece`: figura za koju se potezi dobavljaju
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BROWN or piece.queen:
            moves.update(self.get_moves(row - 1, max(row - 3, -1), -1, piece.color, -1, left))
            moves.update(self.get_moves(row - 1, max(row - 3, -1), -1, piece.color, 1, right))
        if piece.color == WHITE or piece.queen:
            moves.update(self.get_moves(row + 1, min(row + 3, ROWS), 1, piece.color, -1, left))
            moves.update(self.get_moves(row + 1, min(row + 3, ROWS), 1, piece.color, 1, right))

        return moves
    
    def get_moves(self, start, stop, step, color, direction, position, captured = []):
        """
        Funkcija dobavlja poteze u datom pravcu od pocetne figure.
        - `start`: red od kojeg se krece
        - `stop`: krajnji red
        - `step`: korak kojim se krece kroz redove; moze biti +1, kretanje nagore, ili -1, kretanje nadole
        - `color`: boja figure cije poteze dobavljamo
        - `direction`: smer kretanja; moze biti -1 za levo ili +1 za desno
        - `position`: kolona sa trenutne strane (levo ili desno) trenutne figure
        - `captured`: lista figura koje se mogu pojesti u toku poteza
        """
        moves = {}
        last = []
        for row in range(start, stop, step):
            if position < 0 or position >= COLS:
                break
            
            current = self.board[row][position]
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(row, position)] = last + captured
                else:
                    moves[(row, position)] = last
                
                if last:
                    if step == -1:
                        new_row = max(row - 3, -1)
                    else:
                        new_row = min(row + 3, ROWS)
                    moves.update(self.get_moves(row + step, new_row, step, color, -1, position - 1, captured = last))
                    moves.update(self.get_moves(row + step, new_row, step, color, 1, position + 1, captured = last))
                break
            elif current.color == color:
                break
            else:
                last.append(current)

            position += direction
        
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
    
    def evaluate_state(self):
        if self.game_over(WHITE) == "WHITE" or self.game_over(BROWN) == "WHITE":
            return float('inf')
        elif self.game_over(BROWN) == "BROWN" or self.game_over(WHITE) == "BROWN":
            return float('-inf')
        total_pieces = self.brown_left + self.white_left
        if total_pieces >= 17:
            return self.evaluate_state_with_weights(20, 70, 40, 6, 10, 16)
        elif total_pieces >= 10:
            return self.evaluate_state_with_weights(20, 70, 30, 8, 14, 20)
        else:
            return self.evaluate_state_with_weights(20, 70, 20, 10, 20, 24)

    def evaluate_state_with_weights(self, piece_weight, queen_weight, center_bonus, mobility_bonus,
                                    protected_bonus, attack_bonus):
        brown_score = 0
        white_score = 0

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece == 0:
                    continue
                
                piece_value = 0
                
                if piece.queen:
                    piece_value += queen_weight
                else:
                    piece_value += piece_weight
                
                if 2 <= row <= 5 and 2 <= col <= 5:
                    piece_value += center_bonus

                valid_moves = self.get_valid_moves(piece)
                piece_value += mobility_bonus * len(valid_moves)
                for capture in valid_moves.values():
                    if capture:
                        piece_value += attack_bonus

                if self.is_protected(piece):
                    piece_value += protected_bonus
                
                if piece.color == BROWN:
                    brown_score += piece_value
                else:
                    white_score += piece_value

        return white_score - brown_score

    def is_protected(self, piece):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            row, col = piece.row + direction[0], piece.col + direction[1]
            if 0 <= row < ROWS and 0 <= col < COLS:
                neighbor = self.get_piece(row, col)
                if neighbor and neighbor.color == piece.color:
                    return True
        return False
    
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