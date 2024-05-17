from copy import deepcopy
from constants import BROWN, WHITE

def alpha_beta_pruning(board, depth):
    value = max_value(depth, board, WHITE, float('-inf'), float('inf'))
    return get_board(get_children(board, WHITE), value)


def max_value(depth, board, turn, alpha, beta):
    if depth == 0 or board.winner(turn) is not None:
        return board.evaluate_state()
    
    max_val = float('-inf')
    for child in get_children(board, turn):
        max_val = max(max_val, min_value(depth - 1, child, BROWN, alpha, beta))
        alpha = max(alpha, max_val)
        if alpha >= beta:
            break
    
    return max_val

def min_value(depth, board, turn, alpha, beta):
    if depth == 0 or board.winner(turn) is not None:
        return board.evaluate_state()
    
    min_val = float('inf')
    for child in get_children(board, turn):
        min_val = min(min_val, max_value(depth - 1, child, WHITE, alpha, beta))
        beta = min(beta, min_val)
        if alpha >= beta:
            break
    
    return min_val

def get_children(board, turn):
    children = []
    valid_moves = get_all_valid_moves(board, turn)

    for piece, moves in valid_moves.items():
        for move, skip in moves.items():
            new_board = deepcopy(board)
            new_piece = new_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(new_piece, move, new_board, skip)
            children.append(new_board)
    
    return children


def get_all_valid_moves(board, turn):
    valid_moves = {}
    pieces = board.get_pieces_color(turn)

    for piece in pieces:
        valid_moves[piece] = board.get_valid_moves(piece)

    return valid_moves

def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_board(boards, value):
    for board in boards:
        if board.evaluate_state() == value:
            return board
    return None