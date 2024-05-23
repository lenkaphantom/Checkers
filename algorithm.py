import time
from copy import deepcopy
from constants import BROWN, WHITE

transposition_table = {}

def alpha_beta_pruning(board, max_depth, turn, mode):
    start_time = time.time()
    time_limit = 2.8

    def alpha_beta(board, depth, alpha, beta, maximizing_player):
        if depth == 0 or time.time() - start_time > time_limit or board.game_over(WHITE if maximizing_player else BROWN) != None:
            return board.evaluate_state(maximizing_player), board

        board.get_zobrist_key()
        zobrist_key = (board.zobrist_key, depth)

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
                if value == float('inf'):
                    break
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
                if value == float('-inf'):
                    break
                beta = min(beta, value)
                if alpha >= beta:
                    break
            transposition_table[zobrist_key] = (value, best_move)
            return value, best_move

    best_move = None
    previous_best_move = None

    for depth in range(3, max_depth + 1):
        _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), turn == WHITE)
        if best_move is not None:
            previous_best_move = best_move
        if time.time() - start_time > time_limit:
            break

    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

    if best_move is None:
        return previous_best_move

    return best_move

def get_states(board, maximizing_player, mode):
    states = []
    turn = WHITE if maximizing_player else BROWN
    pieces = board.get_pieces_color(turn)
    for piece in pieces:
        valid_moves = []
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

# def minimax(board, max_depth, turn, mode):
#     start_time = time.time()
#     time_limit = 2.7
#     previous_best_move = None

#     def minimax_rec(board, depth, maximizing_player):
#         if depth == 0 or time.time() - start_time > time_limit or board.game_over(WHITE if maximizing_player else BROWN) != None:
#             return board.evaluate_state(maximizing_player), board

#         board.get_zobrist_key()
#         zobrist_key = (board.zobrist_key, depth)

#         if zobrist_key in transposition_table:
#             return transposition_table[zobrist_key]

#         if maximizing_player:
#             value = float('-inf')
#             best_move = None
#             for state in get_states(board, WHITE, mode):
#                 new_value, _ = minimax_rec(state[0], depth - 1, False)
#                 if new_value > value:
#                     value = new_value
#                     best_move = state[0]
#             transposition_table[zobrist_key] = (value, best_move)
#             return value, best_move
#         else:
#             value = float('inf')
#             best_move = None
#             for state in get_states(board, BROWN, mode):
#                 new_value, _ = minimax_rec(state[0], depth - 1, True)
#                 if new_value < value:
#                     value = new_value
#                     best_move = state[0]
#             transposition_table[zobrist_key] = (value, best_move)
#             return value, best_move

#     best_move = None
#     for depth in range(3, max_depth + 1):
#         _, best_move = minimax_rec(board, depth, turn == WHITE)
#         if best_move is not None:
#             previous_best_move = best_move
#         if time.time() - start_time > time_limit:
#             break

#     end_time = time.time()
#     print(f"Time taken: {end_time - start_time}")

#     if best_move is None:
#         return previous_best_move

#     return best_move