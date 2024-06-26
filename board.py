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
    #     Heuristička funkcija koja računa skor na osnovu različitih parametara za svaku boju.
    #     """
    #     if maximizing_player:
    #         if self.game_over(WHITE) == "WHITE":
    #             return float('inf')
    #         elif self.game_over(WHITE) == "BROWN":
    #             return float('-inf')
    #     else:
    #         if self.game_over(BROWN) == "BROWN":
    #             return float('-inf')
    #         elif self.game_over(BROWN) == "WHITE":
    #             return float('inf')

    #     white_score = self.calculate_score(WHITE)
    #     brown_score = self.calculate_score(BROWN)

    #     return white_score - brown_score

    # def calculate_score(self, color):
    #     """
    #     Funkcija koja računa skor za određenu boju.
    #     """
    #     score = 0
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             piece = self.get_piece(row, col)
    #             if piece != 0 and piece.color == color:
    #                 piece_moves = self.get_valid_moves(piece)
    #                 if piece.queen:
    #                     score += 10
    #                     if self.is_safe(row, col):
    #                         score += 5
    #                     if self.is_moveable(piece_moves):
    #                         score += 2
    #                 else:
    #                     score += 1
    #                     if self.is_safe(row, col):
    #                         score += 3
    #                     if self.is_moveable(piece):
    #                         score += 1
    #                     if self.is_promotable_in_one_move(piece_moves, color):
    #                         score += 7
    #                     if self.is_defender(piece):
    #                         score += 2
    #                     elif self.is_attacker(piece):
    #                         score += 2
    #                     elif self.is_central_piece(piece):
    #                         score += 2
    #     return score
    
    # def is_safe(self, row, col):
    #     """
    #     Proverava da li je figura sigurna (pored ivice table).
    #     """
    #     return row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1

    # def is_moveable(self, piece_moves):
    #     """
    #     Proverava da li je figura može da se pomeri (ne računajući prioritet hvatanja).
    #     """
    #     return bool(piece_moves)

    # def is_promotable_in_one_move(self, piece_moves, color):
    #     """
    #     Proverava da li je figura može da se promoviše u jednom potezu.
    #     """
    #     for move in piece_moves:
    #         if color == WHITE and move[0] == ROWS - 1:
    #             return True
    #         elif color == BROWN and move[0] == 0:
    #             return True
    #     return False

    # def is_defender(self, piece):
    #     """
    #     Proverava da li je figura branilac (nalazi se u dva najdonja reda).
    #     """
    #     if piece.color == WHITE:
    #         return piece.row >= ROWS - 2
    #     elif piece.color == BROWN:
    #         return piece.row <= 1

    # def is_attacker(self, piece):
    #     """
    #     Proverava da li je figura napadač (nalazi se u tri najgornja reda).
    #     """
    #     if piece.color == WHITE:
    #         return piece.row <= 2
    #     elif piece.color == BROWN:
    #         return piece.row >= ROWS - 3

    # def is_central_piece(self, piece):
    #     """
    #     Proverava da li je figura centralno pozicionirana (nalazi se na osam centralnih kvadrata table).
    #     """
    #     row, col = piece.row, piece.col
    #     return 2 <= row <= 5 and 2 <= col <= 5
    
    def game_over(self, turn):
        """
        Funkcija koja proverava da li je igra zavrsena.
        """
        if self.brown_left <= 0:
            return "WHITE"
        elif self.white_left <= 0:
            return "BROWN"
        if not self.has_valid_moves_for_color(turn):
            if turn == WHITE:
                return "BROWN"
            else:
                return "WHITE"
        return None

    def evaluate_state(self, maximizing_player):
        """
        Heuristička funkcija koja na osnovu faze igre daje prednost različitim elementima.
        U heuristiku je uključeno i vrednovanje završnog stanja igre.
        Elementi koji se uzimaju u obzir su:
        - broj figura,
        - broj kraljica,
        - broj figura na ivicama table,
        - broj figura u sredini table,
        - broj zaštićenih figura,
        - broj napada,
        - sprečavanje protivnika da dobije kraljicu,
        - napad na protivničku kraljicu.
        """
        white_over = self.game_over(WHITE)
        brown_over = self.game_over(BROWN)

        if maximizing_player:
            if white_over == "WHITE":
                return 100000
            elif white_over == "BROWN":
                return -100000
        else:
            if brown_over == "BROWN":
                return -100000
            elif brown_over == "WHITE":
                return 100000

        total_pieces = self.brown_left + self.white_left
        if total_pieces >= 20:
            return self.evaluation_based_on_phase(10, 60, 5, 10, 5, 5, 10, 5, 15, 15)
        elif total_pieces >= 12:
            return self.evaluation_based_on_phase(15, 75, 7.5, 20, 10, 15, 20, 10, 10, 10)
        else:
            return self.evaluation_based_on_phase(20, 100, 10, 30, 10, 25, 20, 20, 10, 10)

    def evaluation_based_on_phase(self, pawn_weight, queen_weight, safe_pawn, safe_queen,
                                mobility_pawn, mobility_queen, promotion_bonus,
                                defending_pieces, attacking_piece, center_piece):
        white_value = 0
        brown_value = 0

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece == 0:
                    continue

                piece_value = 0

                if piece.queen:
                    piece_value += queen_weight
                else:
                    piece_value += pawn_weight

                if (row == 0 and piece.color == WHITE) or (row == ROWS - 1 and piece.color == BROWN) or col == 0 or col == COLS - 1:
                    if piece.queen:
                        piece_value += safe_queen
                    else:
                        piece_value += safe_pawn

                valid_moves = self.get_valid_moves(piece)
                piece_value += len(valid_moves) * (mobility_queen if piece.queen else mobility_pawn)

                if not piece.queen:
                    piece_value += promotion_bonus * (1 / self.distance_to_promotion(piece))
                    if self.is_promotable_in_one_move(valid_moves, piece.color):
                        piece_value += 2 * promotion_bonus

                if (row <= 1 and piece.color == WHITE) or (row >= ROWS - 2 and piece.color == BROWN):
                    piece_value += defending_pieces
                
                if row == 0 and piece.color == WHITE and (col == 1 or col == 5):
                    piece_value += 2 * defending_pieces
                elif row == ROWS - 1 and piece.color == BROWN and (col == 2 or col == 6):
                    piece_value += 2 * defending_pieces

                if 2 <= row <= 5 and 2 <= col <= 5:
                    piece_value += center_piece
                elif piece.color == WHITE and row >= ROWS - 3:
                    piece_value += attacking_piece
                elif piece.color == BROWN and row <= 2:
                    piece_value += attacking_piece

                if piece.color == BROWN:
                    brown_value += piece_value
                else:
                    white_value += piece_value

        return white_value - brown_value

    def distance_to_promotion(self, piece):
        if piece.color == WHITE:
            return ROWS - 1 - piece.row
        return piece.row
    
    def is_promotable_in_one_move(self, piece_moves, color):
        """
        Proverava da li je figura može da se promoviše u jednom potezu.
        """
        for move in piece_moves:
            if color == WHITE and move[0] == ROWS - 1:
                return True
            elif color == BROWN and move[0] == 0:
                return True
        return False