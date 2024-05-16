from copy import deepcopy
from constants import BROWN, WHITE
import pygame

def minimax(game, depth, maximizing_player, mode):
    """
    Funkcija koja implementira minimax algoritam.
    """
    if depth == 0 or game.winner() != None:
        return game.evaluate(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(game, WHITE, mode):
            evaluation = minimax(move, depth - 1, False)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(game, BROWN, mode):
            evaluation = minimax(move, depth - 1, True)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move
    
def get_all_moves(game, color, mode):
    """
    Funkcija koja vraca sve moguce poteze za odredjenu boju.
    """
    moves = {}
    pieces = game.board.get_pieces_color(color)
    for piece in pieces:
        if mode == 1:
            moves[piece] = game.board.get_forced_valid_moves(piece)
        else:
            moves[piece] = game.board.get_valid_moves(piece)
    return moves