import time
from copy import deepcopy
from constants import BROWN, WHITE

def alpha_beta_pruning(board, depth, turn, mode):
    start_time = time.time()
    time_limit = 2.7

    def alpha_beta(board, depth, alpha, beta, maximizing_player, mode):
        if time.time() - start_time > time_limit:
            return board.evaluate_state(maximizing_player), board

        if depth == 0 or board.game_over(turn):
            return board.evaluate_state(maximizing_player), board
        
        if maximizing_player:
            value = float('-inf')
            best_move = None
            for state in get_states(board, maximizing_player, mode):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, False, mode)
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
            for state in get_states(board, maximizing_player, mode):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, True, mode)
                if new_value < value:
                    value = new_value
                    best_move = state[0]
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

    _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), turn == WHITE, mode)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

    return best_move

def get_states(board, maximizing_player, mode):
    states = []
    if maximizing_player:
        turn = WHITE
    else:
        turn = BROWN
    pieces = board.get_pieces_color(turn)
    for piece in pieces:
        if mode == 1:
            forced_moves = board.get_forced_valid_moves(piece.color)
            if not forced_moves:
                valid_moves = board.get_valid_moves(piece)
            elif piece in forced_moves:
                valid_moves = forced_moves[piece]
            else:
                continue
        else:
            valid_moves = board.get_valid_moves(piece)
        if not valid_moves:
            continue
        for move, capture in valid_moves.items():
            new_board = deepcopy(board)
            new_piece = new_board.get_piece(piece.row, piece.col)
            new_board.move(new_piece, move[0], move[1])
            if capture:
                new_board.remove(capture)
            value = new_board.evaluate_state(maximizing_player)
            states.append((new_board, value))
    return states