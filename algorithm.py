import time
from copy import deepcopy
from constants import BROWN, WHITE

transposition_table = {}

def alpha_beta_pruning(board, depth, turn, mode):
    start_time = time.time()
    time_limit = 2.7

    def alpha_beta(board, depth, alpha, beta, maximizing_player):
        if time.time() - start_time > time_limit:
            return board.evaluate_state(maximizing_player), board

        if depth == 0 or board.game_over(turn):
            return board.evaluate_state(maximizing_player), board

        board.get_zobrist_key()
        zobrist_key = board.zobrist_key

        if zobrist_key in transposition_table:
            return transposition_table[zobrist_key]

        if maximizing_player:
            value = float('-inf')
            best_move = None
            for state in get_states(board, WHITE, mode):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, False)
                if new_value > value:
                    value = new_value
                    best_move = state[0]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            transposition_table[zobrist_key] = (value, best_move)
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for state in get_states(board, BROWN, mode):
                new_value, _ = alpha_beta(state[0], depth - 1, alpha, beta, True)
                if new_value < value:
                    value = new_value
                    best_move = state[0]
                beta = min(beta, value)
                if alpha >= beta:
                    break
            transposition_table[zobrist_key] = (value, best_move)
            return value, best_move

    _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), turn == WHITE)

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