from copy import deepcopy
from constants import BROWN, WHITE

def alpha_beta_pruning(board, depth, turn):
    def alpha_beta(board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_over(turn):
            return board.evaluate_state(), board
        
        if maximizing_player:
            value = float('-inf')
            best_move = None
            for state in get_states(board, turn):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, False)
                if new_value > value:
                    value = new_value
                    best_move = state[0]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for state in get_states(board, turn):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, True)
                if new_value < value:
                    value = new_value
                    best_move = state[0]
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

    _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), turn == BROWN)
    return best_move

def get_states(board, turn):
    states = []
    pieces = board.get_pieces_color(turn)
    for piece in pieces:
        valid_moves = board.get_valid_moves(piece)
        if not valid_moves:
            continue
        for move, capture in valid_moves.items():
            new_board = deepcopy(board)
            new_piece = new_board.get_piece(piece.row, piece.col)
            new_board.move(new_piece, move[0], move[1])
            if capture:
                new_board.remove(capture)
            value = new_board.evaluate_state()
            states.append((new_board, value))
    return states

def change_turn(turn):
    return WHITE if turn == BROWN else BROWN