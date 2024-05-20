import random
from constants import ROWS, COLS

def initialize_zobrist():
    zobrist_table = {}
    pieces = ['white_pawn', 'white_queen', 'brown_pawn', 'brown_queen']
    
    for row in range(ROWS):
        for col in range(COLS):
            for piece in pieces:
                zobrist_table[(row, col, piece)] = random.getrandbits(64)
    
    return zobrist_table

zobrist_table = initialize_zobrist()