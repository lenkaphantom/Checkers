from constants import BROWN, WHITE
from copy import deepcopy

def alpha_beta_pruning(board, depth, turn):
    print(turn)
    states = get_states(board, turn)
    value = max_value(board, float('-inf'), float('inf'), depth, turn)
    print(value)
    for state in states:
        print(state[0])
        print(state[1])
        if state[1] == value:
            return state[0]
    
    return None

def max_value(board, alpha, beta, depth, turn):
    if depth == 0 or board.game_over(turn):
        return board.evaluate_state()
    
    value = float('-inf')
    for state in get_states(board, turn):
        value = max(value, min_value(state[0], alpha, beta, depth - 1, change_turn(turn)))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    
    return value

def min_value(board, alpha, beta, depth, turn):
    if depth == 0 or board.game_over(turn):
        return board.evaluate_state()
    
    value = float('inf')
    for state in get_states(board, turn):
        value = min(value, max_value(state[0], alpha, beta, depth - 1, change_turn(turn)))
        if value <= alpha:
            return value
        beta = min(beta, value)
    
    return value

def get_states(board, turn):
    states = []
    
    pieces = board.get_pieces_color(turn)
    for piece in pieces:
        valid_moves = board.get_valid_moves(piece)
        if not valid_moves:
            continue
        for move, capture in valid_moves.items():
            new_board = deepcopy(board)
            new_board.move(piece, move[0], move[1])
            if capture:
                new_board.remove(capture)
            value = new_board.evaluate_state()
            states.append([new_board, value])
            
    return states
    
def change_turn(turn):
    if turn == BROWN:
        return WHITE
    return BROWN