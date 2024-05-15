import pygame

from constants import *
from board import Board

class Game(object):
    def __init__(self, win, mode):
        self.selected = None
        self.board = Board()
        self.turn = BROWN
        self.valid_moves = {}
        self.win = win
        self.mode = mode

    def update(self):
        """
        Funkcija koja azurira stanje table i koja iscrtava moguce poteze za figuru.
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col, mode):
        """
        Funkcija koja selektovanu figuru, ako ona postoji, pomera u odgovarajuci red i kolonu.
        Ako nije selektovana figura, selektuje se ona koja se nalazi u zadatom redu i koloni
        ako na tom polju figura postoji i ako je iste boje kao igrac koji je na potezu.
        Potom se odredjuju svi validni potezi za tu figuru u zavisnosti od rezima igre.

        - `row`: red u kome se nalazi figura ili na koji figuru treba pomeriti
        - `col`: kolona u kojoj se nalazi figura ili na koju figuru treba pomeriti
        - `mode`: odabrani rezim igre
        """
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = {}
                self.select(row, col, mode)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            if mode == 1:
                forced_moves = self.board.get_forced_valid_moves(piece.color)
                if not forced_moves:
                    self.valid_moves = self.board.get_valid_moves(piece)
                elif piece in forced_moves:
                    self.valid_moves = forced_moves[piece]
            else:
                self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def move(self, row, col):
        """
        Funkcija koja pomera figuru na odgovarajuce polje.
        Ako je potez validan, figura se pomera na to polje i proverava se da li je neka figura pojedena.
        Ako je neka figura pojedena, ona se uklanja sa table.
        Na kraju se menja igrac koji je na potezu.

        - `row`: red na koji se figura pomera
        - `col`: kolona na koju se figura pomera
        """
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
        """
        Funkcija koja iscrtava moguce poteze za figuru.

        - `moves`: lista mogucih poteza
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def change_turn(self):
        """
        Funkcija koja menja igraca koji je na potezu.
        """
        self.valid_moves = {}
        if self.turn == BROWN:
            self.turn = WHITE
        else:
            self.turn = BROWN
            
    def winner(self):
        """
        Funkcija koja proverava da li je neki igrac pobedio.
        """
        if self.board.brown_left <= 0:
            return "WHITE"
        elif self.board.white_left <= 0:
            return "BROWN"
        if not self.board.has_valid_moves_for_color(self.turn):
            if self.turn == BROWN:
                return "WHITE"
            else:
                return "BROWN"
        return None
    
    def draw_winner(self):
        """
        Funkcija koja ispisuje pobednika na ekranu.
        """
        self.win.fill(BEIGE)
        winner = self.winner()
        font = pygame.font.SysFont(None, 100)
        text = font.render(f"{winner} Wins!", True, GREY)
        self.win.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
        pygame.display.update()