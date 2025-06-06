from .pieces import *

turn = 'W'
in_check = ''
king_loc = []
fifty_move_stalemate = 0
repetition = 0
# - means no special moves
# 0 means no moves for kings, rooks and pawns
# removing the 0 means the piece has moved for kings and rooks
# 2 means the first move was a double move for pawns
# 3 means the pawn is on the rank for it to capture by en passant
# [1] = B means the bishop is on the black squares and vice versa
board = [['R0W', 'N-W', 'BBW', 'Q-W', 'K0W', 'BWW', 'N-W', 'R0W']] + [['P-W' for _ in range(8)]] + [
    ['  ' for _ in range(8)] for _ in range(4)] + [['P-B' for _ in range(8)]] + [
            ['R0B', 'N-B', 'BWB', 'Q-B', 'K0B', 'BBB', 'N-B', 'R0B']]
check_repetition = []


# xi, yi are the initial coordinates of the piece to move
def move(pos):
    global turn
    global in_check
    global king_loc
    global fifty_move_stalemate
    global repetition
    try:
        xi, yi, xn, yn = pos[0], int(pos[1]), pos[2], int(pos[3])  # if the input is too short or not correct types
    except Exception:
        print('That is not a valid move')
        return False
    if ord(xi) - 97 < 0 or ord(xn) - 97 < 0 or len(pos) > 4:  # if the input is too long or not correct types
        print('That is not a valid move')
        return False
    # inverse pieces to work with indexing
    yi, xi, yn, xn = ord(xi) - 97, yi - 1, ord(xn) - 97, yn - 1  # format the pieces to work with the array
    if board[xi][yi][0] == ' ':  # not a piece to move
        print('That is not a valid move')
        return False
    if board[xi][yi][-1] == turn:  # check if the color of the piece to move is the same as the turn
        if board[xi][yi][0] == 'P' and not [xn, yn] in PawnCheck.valid_moves(yi, xi, turn, board, in_check, king_loc):
            print('Pawn move not allowed')
            return False
        elif board[xi][yi][0] == 'R' and not [xn, yn] in RookCheck.valid_moves(yi, xi, turn, board, in_check, king_loc):
            print('Rook move not allowed')
            return False
        elif board[xi][yi][0] == 'N' and not [xn, yn] in NightCheck.valid_moves(yi, xi, turn, board, in_check,
                                                                                king_loc):
            print('Knight move not allowed')
            return False
        elif board[xi][yi][0] == 'B' and not [xn, yn] in BishopCheck.valid_moves(yi, xi, turn, board, in_check,
                                                                                 king_loc):
            print('Bishop move not allowed')
            return False
        elif board[xi][yi][0] == 'K' and not [xn, yn] in KingCheck.valid_moves(yi, xi, turn, board, in_check, king_loc):
            print('King move not allowed')
            return False
        elif board[xi][yi][0] == 'Q' and not [xn, yn] in QueenCheck.valid_moves(yi, xi, turn, board, in_check,
                                                                                king_loc):
            print('Queen move not allowed')
            return False
        # check if capture by en passant is not done immediately
        for i in range(8):
            for j in range(8):
                if board[i][j][-1] == turn:
                    if board[i][j][0] == 'P' and board[i][j][1] == '2' and board[xi][yi] != board[i][j]:
                        if (turn == 'W' and i == 4) or (turn == 'B' and i == 3):
                            board[i][j] = 'P-' + board[i][j][-1]
        if board[xi][yi][0] == 'K' and abs(yn - yi) == 2:  # move the rook if castling
            board[xi][yi + (yn - yi - [1 if yn > yi else -1][0])] = board[xi][
                yi + (yn - yi - [-1 if yn > yi else 2][0])]
            board[xi][yi + (yn - yi - [-1 if yn > yi else 2][0])] = '  '
        if board[xi][yi][0] == 'P' and (xn == 7 or xn == 0):  # pawn promotion
            board[xn][yn] = 'Q-' + board[xi][yi][-1]
            if board[xn][yn] != '  ':
                fifty_move_stalemate = 0
        elif board[xi][yi][0] == 'P' and yi != yn and board[xi][yi][1] == '2':
            board[xn][yn] = 'P' + '-' + turn
            board[xi][yi + (yn - yi)] = '  '  # taking with en passant
            fifty_move_stalemate = 0
        else:
            board[xn][yn] = board[xi][yi]
            if board[xn][yn] != '  ':
                fifty_move_stalemate = 0
        if board[xi][yi][0] == 'P':
            fifty_move_stalemate = 0
        else:
            fifty_move_stalemate += 1
        board[xi][yi] = '  '  # replace the original square with empty
        if board[xn][yn][0] == 'K' or board[xn][yn][0] == 'R':
            board[xn][yn] = board[xn][yn][0] + '-' + turn  # check if the king or rook have moved to help with castling
        elif board[xn][yn][0] == 'P' and (xn == xi + 2 or xn == xi - 2):
            board[xn][yn] = 'P2' + turn  # add value of 2 to pawn to help with checking for en passant
        elif board[xn][yn][0] == 'P' and (yn != yi or (board[xn][yn][-1] == 'W' and xn > 4) or (
                board[xn][yn][-1] == 'B' and xn < 3)):
            board[xn][yn] = 'P-' + turn  # check for taking or en passant to stop further en passant
        all_moves = all_possible_moves(turn, board, in_check, king_loc)
        # see if the king is in check
        for x in range(8):
            for y in range(8):
                if board[x][y][0:3:2] == 'K' + ['W' if turn == 'B' else 'B'][0]:
                    king_loc = [x, y]  # find the position of the king
                    break
        if king_loc in all_moves:  # check if the king is in check
            in_check = ['W' if turn == 'B' else 'B'][0]
        # check for checkmate
        turn = ['W' if turn == 'B' else 'B'][0]
        # ---------------------------- CALCULATE HERE TO FIND ALL MOVES FOR PIECES ----------------------------
        if len(all_possible_moves(turn, board, in_check, king_loc)) == 0:
            print(f"Checkmate by {['Black' if turn == 'W' else 'White'][0]}!")
            exit()
        if fifty_move_stalemate == 50:
            print('Fifty Move Stalemate')
            exit()
        # check for triple repetition
        for _ in range(len(check_repetition)):
            if f'{board}' in check_repetition:
                repetition += 1
                break
        check_repetition.append(f'{board}')
        if repetition == 3:
            print('Stalemate by Repetition')
            exit()
        pieces_left = []
        pieces_left_with_info = []
        for a in range(8):
            for b in range(8):
                if board[a][b] != '  ':
                    pieces_left.append(board[a][b][0:3:2])
                    pieces_left_with_info.append(board[a][b])
        if len(pieces_left) == 2:
            print('Stalemate by Insufficient Material (2 Kings)')
            exit()
        elif len(pieces_left) == 3 and ('NW' in pieces_left or 'NB' in pieces_left):
            print('Stalemate by Insufficient Material (2 Kings and a Knight)')
            exit()
        elif len(pieces_left) == 3 and ('BW' in pieces_left or 'BB' in pieces_left):
            print('Stalemate by Insufficient Material (2 Kings and a Bishop)')
            exit()
        elif len(pieces_left) == 4 and (('BBW' in pieces_left_with_info and 'BBB' in pieces_left_with_info) or (
                'BWW' in pieces_left_with_info and 'BWB' in pieces_left_with_info)):
            print('Stalemate by Insufficient Material (2 Kings and 2 Bishops on the same colour)')
            exit()
        return True
    print('Move not allowed (it is not your turn)')


def any_move(pos):
    xi, yi, xn, yn = pos[0], int(pos[1]), pos[2], int(pos[3])
    yi, xi, yn, xn = ord(xi) - 97, yi - 1, ord(xn) - 97, yn - 1
    original = deepcopy(board[xn][yn])
    board[xn][yn] = board[xi][yi]
    board[xi][yi] = original
    # show_pieces()


def add_score(board, i, j):
    score = 0
    if board[i][j][0] == 'P':
        score += 10
    if board[i][j][0] == 'N':
        score += 30
    if board[i][j][0] == 'B':
        score += 30
    if board[i][j][0] == 'R':
        score += 50
    if board[i][j][0] == 'Q':
        score += 90
    if board[i][j][0] == 'K':
        score += 900
    return score
