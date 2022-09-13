from .game import *
from math import inf
from .evaluation import *

depth = 3


def minimax(depth, maximizing_player, maximizing_colour, alpha=-inf, beta=inf):
    opposite_colour = 'W' if maximizing_colour == 'B' else 'B'
    cur_colour = maximizing_colour if maximizing_player else opposite_colour
    if depth == 0:
        return evaluate_board(board) if maximizing_colour == 'W' else -evaluate_board(board)
    moves = labelled_all_possible_moves(cur_colour, board, in_check, king_loc)
    # print(cur_colour)
    if maximizing_player:  # max
        best_move = -inf
        for move in moves:
            move = move[0]
            any_move(move)
            value = minimax(depth - 1, False, maximizing_colour, alpha, beta)
            any_move(move[2:] + move[0:2])
            best_move = max(best_move, value)
            alpha = max(alpha, value)
        return best_move
    else:  # min
        best_move = inf
        for move in moves:
            move = move[0]
            any_move(move)
            value = minimax(depth - 1, True, maximizing_colour, alpha, beta)
            any_move(move[2:] + move[0:2])
            best_move = min(best_move, value)
            beta = min(beta, value)
        return best_move


def minimaxRoot(depth, maximizing_colour):
    moves = labelled_all_possible_moves(maximizing_colour, board, in_check, king_loc)
    best_move = -inf
    best_move_found = int()
    for move in moves:
        move = move[0]
        any_move(move)
        value = minimax(depth - 1, False, maximizing_colour, -inf, inf)
        any_move(move[2:] + move[0:2])
        if value >= best_move:
            best_move = value
            best_move_found = move

    return best_move_found
