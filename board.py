from typing import Any
import pygame
from constants import *
from piece import Piece
from zobrist_hashing import zobrist_table

class Board(object):
    def __init__(self):
        self.board = []
        self.brown_left = self.white_left = 12
        self.brown_queens = self.white_queens = 0
        self.create_board()
        self.zobrist_key = 0
        
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

    def get_zobrist_key(self):
        key = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece != 0:
                    if piece.color == WHITE:
                        if piece.queen:
                            key ^= zobrist_table[(row, col, 'white_queen')]
                        else:
                            key ^= zobrist_table[(row, col, 'white_pawn')]
                    else:
                        if piece.queen:
                            key ^= zobrist_table[(row, col, 'brown_queen')]
                        else:
                            key ^= zobrist_table[(row, col, 'brown_pawn')]

        self.zobrist_key = key

    def update_zobrist_key(self, piece, row, col):
        if piece.color == WHITE:
            if piece.queen:
                self.zobrist_key ^= zobrist_table[(row, col, 'white_queen')]
            else:
                self.zobrist_key ^= zobrist_table[(row, col, 'white_pawn')]
        else:
            if piece.queen:
                self.zobrist_key ^= zobrist_table[(row, col, 'brown_queen')]
            else:
                self.zobrist_key ^= zobrist_table[(row, col, 'brown_pawn')]

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
        self.update_zobrist_key(piece, piece.row, piece.col)

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if not piece.queen:
                piece.make_queen()
                if piece.color == BROWN:
                    self.brown_queens += 1
                else:
                    self.white_queens += 1

        self.update_zobrist_key(piece, row, col)

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
            
            current = self.get_piece(row, position)
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
            if piece != 0:
                self.board[piece.row][piece.col] = 0
                if piece.color == BROWN:
                    self.brown_left -= 1
                    if piece.queen:
                        self.brown_queens -= 1
                else:
                    self.white_left -= 1
                    if piece.queen:
                        self.white_queens -= 1
                self.update_zobrist_key(piece, piece.row, piece.col)

    # def evaluate_state(self, maximizing_player):
    #     """
    #     Heuristička funkcija koja na osnovu faze igre daje prednost različitim elementima.
    #     U heuristiku je uključeno i vrednovanje završnog stanja igre.
    #     Elementi koji se uzimaju u obzir su:
    #     - broj figura,
    #     - broj kraljica,
    #     - broj figura na ivicama table,
    #     - broj figura u sredini table,
    #     - broj zaštićenih figura,
    #     - broj napada,
    #     - sprečavanje protivnika da dobije kraljicu,
    #     - napad na protivničku kraljicu.
    #     """
    #     white_over = self.game_over(WHITE)
    #     brown_over = self.game_over(BROWN)
    #     if maximizing_player:
    #         if white_over == "WHITE":
    #             return float('inf')
    #         elif white_over == "BROWN":
    #             return float('-inf')
    #     else:
    #         if brown_over == "BROWN":
    #             return float('-inf')
    #         elif brown_over == "WHITE":
    #             return float('inf')

    #     total_pieces = self.brown_left + self.white_left
    #     if total_pieces >= 16:
    #         return self.evaluation_based_on_phase(
    #             pawn_weight=10, queen_weight=40, safe_pawn=5, safe_queen=10,
    #             mobility_pawn=5, mobility_queen=5, promotion_bonus=15,
    #             defending_pieces=5, attacking_piece=10, center_piece=20, multiple_jumps_bonus=30
    #         )
    #     elif total_pieces >= 8:
    #         return self.evaluation_based_on_phase(
    #             pawn_weight=5, queen_weight=30, safe_pawn=5, safe_queen=15,
    #             mobility_pawn=10, mobility_queen=10, promotion_bonus=20,
    #             defending_pieces=20, attacking_piece=15, center_piece=10, multiple_jumps_bonus=15
    #         )
    #     else:
    #         return self.evaluation_based_on_phase(
    #             pawn_weight=5, queen_weight=50, safe_pawn=10, safe_queen=20,
    #             mobility_pawn=5, mobility_queen=20, promotion_bonus=10,
    #             defending_pieces=10, attacking_piece=15, center_piece=5, multiple_jumps_bonus=10
    #         )

    # def evaluation_based_on_phase(self, pawn_weight, queen_weight, safe_pawn, safe_queen,
    #                           mobility_pawn, mobility_queen, promotion_bonus,
    #                           defending_pieces, attacking_piece, center_piece, multiple_jumps_bonus):
    #     white_value = 0
    #     brown_value = 0

    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             piece = self.get_piece(row, col)
    #             if piece == 0:
    #                 continue

    #             piece_value = 0

    #             if (row == 0 and piece.color == WHITE) or (row == ROWS - 1 and piece.color == BROWN) or col == 0 or col == COLS - 1:
    #                 if piece.queen:
    #                     piece_value += safe_queen
    #                 else:
    #                     piece_value += safe_pawn

    #             valid_moves = self.get_valid_moves(piece)
    #             for move, capture in valid_moves.items():
    #                 if capture:
    #                     piece_value += attacking_piece * self.captured_queen(capture)
    #                     if len(capture) > 1:
    #                         piece_value += multiple_jumps_bonus
    #                 elif piece.queen:
    #                     piece_value += mobility_queen
    #                 else:
    #                     piece_value += mobility_pawn

    #             if not piece.queen:
    #                 piece_value += self.pieces_to_promote(piece.color) * promotion_bonus

    #             if (row <= 1 and piece.color == WHITE) or (row >= ROWS - 2 and piece.color == BROWN):
    #                 piece_value += defending_pieces

    #             if 2 <= row <= 5 and 2 <= col <= 5:
    #                 piece_value += center_piece

    #             if piece.color == BROWN:
    #                 brown_value += piece_value
    #             else:
    #                 white_value += piece_value

    #     white_value += self.white_queens * queen_weight + (self.white_left - self.white_queens) * pawn_weight
    #     brown_value += self.brown_queens * queen_weight + (self.brown_left - self.brown_queens) * pawn_weight

    #     return white_value - brown_value

    # def pieces_to_promote(self, color):
    #     pieces = self.get_pieces_color(color)
    #     count = 0

    #     for piece in pieces:
    #         val_moves = self.get_valid_moves(piece)
    #         for move in val_moves:
    #             if color == WHITE:
    #                 if move[0] == ROWS - 1:
    #                     count += 1
    #             else:
    #                 if move[0] == 0:
    #                     count += 1

    #     return count
    
    # def captured_queen(self, captured):
    #     total = 0
    #     for piece in captured:
    #         if piece.queen:
    #             total += 1
    #     return total

    def evaluate_state(self, maximizing_player):
        """
        Heuristička funkcija koja računa skor na osnovu različitih parametara za svaku boju.
        """
        white_over = self.game_over(WHITE)
        brown_over = self.game_over(BROWN)

        if maximizing_player:
            if white_over == "WHITE":
                return float('inf')
            elif white_over == "BROWN":
                return float('-inf')
            elif white_over == "DRAW":
                return 0
        else:
            if brown_over == "BROWN":
                return float('-inf')
            elif brown_over == "WHITE":
                return float('inf')
            
        weights = [5, 7.5, 4, 2.5, 0.5, -3, 3]

        white_score = self.calculate_score(WHITE)
        brown_score = self.calculate_score(BROWN)

        total_score = 0

        for i in range(len(weights)):
            total_score += weights[i] * (white_score[i] - brown_score[i])

        return total_score

    def calculate_score(self, color):
        """
        Funkcija koja računa skor za određenu boju.
        """
        score = [0, 0, 0, 0, 0, 0, 0]
        if color == WHITE:
            score[0] = self.white_left - self.white_queens
            score[1] = self.white_queens
        else:
            score[0] = self.brown_left - self.brown_queens
            score[1] = self.brown_queens
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    if row == ROWS - 1 and color == BROWN:
                        score[2] += 1
                        score[6] += 1
                        continue
                    if row == 0 and color == WHITE:
                        score[2] += 1
                        score[6] += 1
                        continue

                    if row == 3 or row == 4:
                        if 2 <= col <= 5:
                            score[3] += 1
                        else:
                            score[4] += 1

                    if color == BROWN:
                        if row > 0 and 0 < col < 7:
                            temp_piece1 = self.get_piece(row - 1, col - 1)
                            temp_piece2 = self.get_piece(row - 1, col + 1)
                            if temp_piece1 != 0 and temp_piece1.color == WHITE and self.get_piece(row + 1, col + 1) == 0:
                                score[5] += 1
                            if temp_piece2 != 0 and temp_piece2.color == WHITE and self.get_piece(row + 1, col - 1) == 0:
                                score[5] += 1
                        
                        if row < 7:
                            if col == 0 or col == 7:
                                score[6] += 1
                            else:
                                temp_piece1 = self.get_piece(row + 1, col - 1)
                                temp_piece2 = self.get_piece(row + 1, col + 1)
                                if (temp_piece1 != 0 and (temp_piece1.color == WHITE or not temp_piece1.queen)) and (temp_piece2 != 0 and (temp_piece2.color == WHITE or not temp_piece2.queen)):
                                    score[6] += 1
                    else:
                        if row < 7 and 0 < col < 7:
                            temp_piece1 = self.get_piece(row + 1, col - 1)
                            temp_piece2 = self.get_piece(row + 1, col + 1)
                            if temp_piece1 != 0 and temp_piece1.color == BROWN and self.get_piece(row - 1, col + 1) == 0:
                                score[5] += 1
                            if temp_piece2 != 0 and temp_piece2.color == BROWN and self.get_piece(row - 1, col - 1) == 0:
                                score[5] += 1

                        if row > 0:
                            if col == 0 or col == 7:
                                score[6] += 1
                            else:
                                temp_piece1 = self.get_piece(row - 1, col - 1)
                                temp_piece2 = self.get_piece(row - 1, col + 1)
                                if (temp_piece1 != 0 and (temp_piece1.color == BROWN or not temp_piece1.queen)) and (temp_piece2 != 0 and (temp_piece2.color == BROWN or not temp_piece2.queen)):
                                    score[6] += 1

        return score
    
    def game_over(self, turn):
        """
        Funkcija koja proverava da li je igra zavrsena.
        """
        if self.brown_left <= 0:
            return "WHITE"
        elif self.white_left <= 0:
            return "BROWN"
        if not self.has_valid_moves_for_color(turn):
            new_turn = BROWN if turn == WHITE else WHITE
            if not self.has_valid_moves_for_color(new_turn):
                return "DRAW"
            elif turn == WHITE:
                return "BROWN"
            else:
                return "WHITE"
        return None