# indexing the board is reversed with coordinates here due to the way the matrix has been created
# the coordinates are referencing their position by n-1 in the classes (n-1 is used to help with indexing)
from copy import deepcopy

recursion1 = 0
recursion2 = 0


def in_check_moves(xi, yi, turn, board, in_check, king_loc, moves):
    global recursion2
    if recursion2 < 1:
        moves_check = []  # calculate if when a piece is moved, it brings the king out of check
        for i in moves:
            reverse_move_dest = deepcopy(board[i[0]][i[1]])
            reverse_move_orig = deepcopy(board[yi][xi])
            board[i[0]][i[1]] = board[yi][xi]
            board[yi][xi] = '  '
            for x in range(8):
                for y in range(8):
                    if board[x][y][0:3:2] == 'K' + turn:
                        king_loc = [x, y]
                        break
            recursion2 += 1
            all_moves = all_possible_moves(['W' if turn == 'B' else 'B'][0], board, in_check, king_loc)
            recursion2 -= 1
            if king_loc not in all_moves:
                moves_check.append(i)
            board[i[0]][i[1]] = reverse_move_dest
            board[yi][xi] = reverse_move_orig
        return moves_check
    return moves


class Pawn:
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        try:
            moves = []
            if turn == 'W':
                if yi == 1 and board[yi + 2][xi][0] == ' ' and board[yi + 1][xi][0] == ' ':
                    moves.append([yi + 2, xi])  # double moves
                if board[yi + 1][xi][0] == ' ':
                    moves.append([yi + 1, xi])  # single moves
                if xi != 7:
                    if board[yi + 1][xi + 1][-1] == 'B':
                        moves.append([yi + 1, xi + 1])  # taking to the sides
                    if board[yi][xi][1] == '2' and board[yi][xi + 1][1] == '3':
                        moves.append([yi + 1, xi + 1])
                if xi != 0:
                    if board[yi + 1][xi - 1][-1] == 'B':
                        moves.append([yi + 1, xi - 1])
                    if board[yi][xi][1] == '2' and board[yi][xi - 1][1] == '3':
                        moves.append([yi + 1, xi - 1])  # en passant
            if turn == 'B':
                if yi == 6 and board[yi - 2][xi][0] == ' ' and board[yi - 1][xi][0] == ' ':
                    moves.append([yi - 2, xi])
                if board[yi - 1][xi][0] == ' ':
                    moves.append([yi - 1, xi])
                if xi != 7:
                    if board[yi - 1][xi + 1][-1] == 'W':
                        moves.append([yi - 1, xi + 1])
                    if board[yi][xi][1] == '2' and board[yi][xi + 1][1] == '3':
                        moves.append([yi - 1, xi - 1])
                if xi != 0:
                    if board[yi - 1][xi - 1][-1] == 'W':
                        moves.append([yi - 1, xi - 1])
                    if board[yi][xi][1] == '2' and board[yi][xi - 1][1] == '3':
                        moves.append([yi - 1, xi + 1])
            return in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)
        except:
            return []


class Rook:
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        moves = []
        for i in range(yi + 1, 8):  # forwards
            if yi + (i - yi) > 7:
                break
            if board[i][xi][0] == ' ':
                moves.append([i, xi])
            elif board[i][xi][-1] == turn:  # check if destination is the same colour
                break
            elif board[i][xi][-1] != turn:  # check if destination is the other colour
                moves.append([i, xi])
                break
        for i in range(yi):  # backwards
            if yi + (i - yi) < 0:
                break
            i = yi - i - 1
            if board[i][xi][0] == ' ':
                moves.append([i, xi])
            elif board[i][xi][-1] == turn:
                break
            elif board[i][xi][-1] != turn:
                moves.append([i, xi])
                break
        for i in range(xi + 1, 8):  # right
            if xi + (i - xi) > 7:
                break
            if board[yi][i][0] == ' ':
                moves.append([yi, i])
            elif board[yi][i][-1] == turn:
                break
            elif board[yi][i][-1] != turn:
                moves.append([yi, i])
                break
        for i in range(xi):  # left
            if xi + (i - xi) < 0:
                break
            i = xi - i - 1
            if board[yi][i][0] == ' ':
                moves.append([yi, i])
            elif board[yi][i][-1] == turn:
                break
            elif board[yi][i][-1] != turn:
                moves.append([yi, i])
                break
        return in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)


class Night:
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        moves = []
        # work out all 8 cases for knight moves
        if 0 <= yi + 2 <= 7 and 0 <= xi + 1 <= 7:
            if turn != board[yi + 2][xi + 1][-1]:
                moves.append([yi + 2, xi + 1])
        if 0 <= yi + 2 <= 7 and 0 <= xi - 1 <= 7:
            if turn != board[yi + 2][xi - 1][-1]:
                moves.append([yi + 2, xi - 1])
        if 0 <= yi - 2 <= 7 and 0 <= xi + 1 <= 7:
            if turn != board[yi - 2][xi + 1][-1]:
                moves.append([yi - 2, xi + 1])
        if 0 <= yi - 2 <= 7 and 0 <= xi - 1 <= 7:
            if turn != board[yi - 2][xi - 1][-1]:
                moves.append([yi - 2, xi - 1])
        if 0 <= yi + 1 <= 7 and 0 <= xi + 2 <= 7:
            if turn != board[yi + 1][xi + 2][-1]:
                moves.append([yi + 1, xi + 2])
        if 0 <= yi - 1 <= 7 and 0 <= xi + 2 <= 7:
            if turn != board[yi - 1][xi + 2][-1]:
                moves.append([yi - 1, xi + 2])
        if 0 <= yi + 1 <= 7 and 0 <= xi - 2 <= 7:
            if turn != board[yi + 1][xi - 2][-1]:
                moves.append([yi + 1, xi - 2])
        if 0 <= yi - 1 <= 7 and 0 <= xi - 2 <= 7:
            if turn != board[yi - 1][xi - 2][-1]:
                moves.append([yi - 1, xi - 2])
        return in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)


class Bishop:
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        moves = []
        for i in range(1, 8):  # top left
            if xi - i < 0 or yi + i > 7:
                break
            if board[yi + i][xi - i][0] == ' ':
                moves.append([yi + i, xi - i])
            elif board[yi + i][xi - i][-1] == turn:  # check if destination is the same colour
                break
            elif board[yi + i][xi - i][-1] != turn:  # check if destination is the other colour
                moves.append([yi + i, xi - i])
                break
        for i in range(1, 8):  # top right
            if xi + i > 7 or yi + i > 7:
                break
            if board[yi + i][xi + i][0] == ' ':
                moves.append([yi + i, xi + i])
            elif board[yi + i][xi + i][-1] == turn:
                break
            elif board[yi + i][xi + i][-1] != turn:
                moves.append([yi + i, xi + i])
                break
        for i in range(1, 8):  # bottom left
            if xi - i < 0 or yi - i < 0:
                break
            if board[yi - i][xi - i][0] == ' ':
                moves.append([yi - i, xi - i])
            elif board[yi - i][xi - i][-1] == turn:
                break
            elif board[yi - i][xi - i][-1] != turn:
                moves.append([yi - i, xi - i])
                break
        for i in range(1, 8):  # bottom right
            if xi + i > 7 or yi - i < 0:
                break
            if board[yi - i][xi + i][0] == ' ':
                moves.append([yi - i, xi + i])
            elif board[yi - i][xi + i][-1] == turn:
                break
            elif board[yi - i][xi + i][-1] != turn:
                moves.append([yi - i, xi + i])
                break
        return in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)


class King:
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        moves = []
        if 0 <= yi + 1 <= 7 and 0 <= xi + 1 <= 7:
            if turn != board[yi + 1][xi + 1][-1]:
                moves.append([yi + 1, xi + 1])
        if 0 <= yi + 1 <= 7 and 0 <= xi - 1 <= 7:
            if turn != board[yi + 1][xi - 1][-1]:
                moves.append([yi + 1, xi - 1])
        if 0 <= yi - 1 <= 7 and 0 <= xi + 1 <= 7:
            if turn != board[yi - 1][xi + 1][-1]:
                moves.append([yi - 1, xi + 1])
        if 0 <= yi - 1 <= 7 and 0 <= xi - 1 <= 7:
            if turn != board[yi - 1][xi - 1][-1]:
                moves.append([yi - 1, xi - 1])
        if 0 <= yi + 1 <= 7:
            if turn != board[yi + 1][xi][-1]:
                moves.append([yi + 1, xi])
        if 0 <= yi - 1 <= 7:
            if turn != board[yi - 1][xi][-1]:
                moves.append([yi - 1, xi])
        if 0 <= xi + 1 <= 7:
            if turn != board[yi][xi + 1][-1]:
                moves.append([yi, xi + 1])
        if 0 <= xi - 1 <= 7:
            if turn != board[yi][xi - 1][-1]:
                moves.append([yi, xi - 1])
        if in_check != turn:
            if board[yi][xi][1] == '0' and [yi, xi] == [0, 4]:  # castling king side for white
                if board[yi][xi + 3][1] == '0' and board[yi][xi + 2][0] == ' ' and board[yi][xi + 1][0] == ' ':
                    moves = king_two_squares_check(xi, yi, board, turn, in_check, moves, 1, 2)
            if board[yi][xi][1] == '0' and [yi, xi] == [0, 4]:  # castling queen side for white
                if board[yi][xi - 4][1] == '0' and board[yi][xi - 2][0] == ' ' and board[yi][xi - 1][0] == ' ':
                    moves = king_two_squares_check(xi, yi, board, turn, in_check, moves, -1, -2)
            if board[yi][xi][1] == '0' and [yi, xi] == [7, 4]:  # castling king side for black
                if board[yi][xi + 3][1] == '0' and board[yi][xi + 2][0] == ' ' and board[yi][xi + 1][0] == ' ':
                    moves = king_two_squares_check(xi, yi, board, turn, in_check, moves, 1, 2)
            if board[yi][xi][1] == '0' and [yi, xi] == [7, 4]:  # castling queen side for black
                if board[yi][xi - 4][1] == '0' and board[yi][xi - 2][0] == ' ' and board[yi][xi - 1][0] == ' ':
                    moves = king_two_squares_check(xi, yi, board, turn, in_check, moves, -1, -2)
        # check if the king is moving into check
        global recursion1
        if recursion1 < 1:  # prevent infinite recursion
            recursion1 += 1
            moves_check = []
            for i in moves:
                reverse_move_dest = deepcopy(board[i[0]][i[1]])
                reverse_move_orig = deepcopy(board[yi][xi])
                board[i[0]][i[1]] = board[yi][xi]
                board[yi][xi] = '  '
                all_moves = all_possible_moves(['W' if turn == 'B' else 'B'][0], board, in_check, [i[0], i[1]])
                if [i[0], i[1]] not in all_moves:
                    moves_check.append(i)
                board[i[0]][i[1]] = reverse_move_dest
                board[yi][xi] = reverse_move_orig
            moves = moves_check
            recursion1 -= 1
        return in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)


def king_two_squares_check(xi, yi, board, turn, in_check, moves, a, b):
    # check that the square next to the king is not in check
    reverse_move_dest = deepcopy(board[yi][xi + a])
    reverse_move_orig = deepcopy(board[yi][xi])
    board[yi][xi + a] = board[yi][xi]
    board[yi][xi] = '  '
    all_moves = all_possible_moves(['W' if turn == 'B' else 'B'][0], board, in_check, [yi, xi + a])
    if [yi, xi + a] not in all_moves:
        moves.append([yi, xi + b])
    board[yi][xi + a] = reverse_move_dest
    board[yi][xi] = reverse_move_orig
    return moves


class Queen:  # Might be able to shorten this to the commented code
    def valid_moves(self, xi, yi, turn, board, in_check, king_loc):
        moves = []
        # RookCheck = Rook()
        # BishopCheck = Bishop()
        # RookMoves = RookCheck.valid_moves(xi, yi, turn, board)
        # BishopMoves = BishopCheck.valid_moves(xi, yi, turn, board)
        # moves = RookMoves + BishopMoves
        for i in range(1, 8):  # top left
            if xi - i < 0 or yi + i > 7:
                break
            if board[yi + i][xi - i][0] == ' ':
                moves.append([yi + i, xi - i])
            elif board[yi + i][xi - i][-1] == turn:  # check if destination is the same colour
                break
            elif board[yi + i][xi - i][-1] != turn:  # check if destination is the other colour
                moves.append([yi + i, xi - i])
                break
        for i in range(1, 8):  # top right
            if xi + i > 7 or yi + i > 7:
                break
            if board[yi + i][xi + i][0] == ' ':
                moves.append([yi + i, xi + i])
            elif board[yi + i][xi + i][-1] == turn:
                break
            elif board[yi + i][xi + i][-1] != turn:
                moves.append([yi + i, xi + i])
                break
        for i in range(1, 8):  # bottom left
            if xi - i < 0 or yi - i < 0:
                break
            if board[yi - i][xi - i][0] == ' ':
                moves.append([yi - i, xi - i])
            elif board[yi - i][xi - i][-1] == turn:
                break
            elif board[yi - i][xi - i][-1] != turn:
                moves.append([yi - i, xi - i])
                break
        for i in range(1, 8):  # bottom right
            if xi + i > 7 or yi - i < 0:
                break
            if board[yi - i][xi + i][0] == ' ':
                moves.append([yi - i, xi + i])
            elif board[yi - i][xi + i][-1] == turn:
                break
            elif board[yi - i][xi + i][-1] != turn:
                moves.append([yi - i, xi + i])
                break
        for i in range(yi + 1, 8):  # forwards
            if yi + (i - yi) > 7:
                break
            if board[i][xi][0] == ' ':
                moves.append([i, xi])
            elif board[i][xi][-1] == turn:  # check if destination is the same colour
                break
            elif board[i][xi][-1] != turn:  # check if destination is the other colour
                moves.append([i, xi])
                break
        for i in range(yi):  # backwards
            if yi + (i - yi) < 0:
                break
            i = yi - i - 1
            if board[i][xi][0] == ' ':
                moves.append([i, xi])
            elif board[i][xi][-1] == turn:
                break
            elif board[i][xi][-1] != turn:
                moves.append([i, xi])
                break
        for i in range(xi + 1, 8):  # right
            if xi + (i - xi) > 7:
                break
            if board[yi][i][0] == ' ':
                moves.append([yi, i])
            elif board[yi][i][-1] == turn:
                break
            elif board[yi][i][-1] != turn:
                moves.append([yi, i])
                break
        for i in range(xi):  # left
            if xi + (i - xi) < 0:
                break
            i = xi - i - 1
            if board[yi][i][0] == ' ':
                moves.append([yi, i])
            elif board[yi][i][-1] == turn:
                break
            elif board[yi][i][-1] != turn:
                moves.append([yi, i])
                break
        if in_check == turn:
            moves_check = in_check_moves(xi, yi, turn, board, in_check, king_loc, moves)
            return moves_check
        else:
            return moves


PawnCheck, RookCheck, NightCheck, BishopCheck, KingCheck, QueenCheck = Pawn(), Rook(), Night(), Bishop(), King(), Queen()


def all_possible_moves(turn, board, in_check, king_loc):  # for the colour which turn it is
    if recursion1 == 0 or recursion2 == 0:
        moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j][-1] == turn:
                    if board[i][j][0] == 'P':
                        # moves.append('P')
                        moves.append(PawnCheck.valid_moves(j, i, turn, board, in_check, king_loc))
                    elif board[i][j][0] == 'R':
                        # moves.append('R')
                        moves.append(RookCheck.valid_moves(j, i, turn, board, in_check, king_loc))
                    elif board[i][j][0] == 'N':
                        # moves.append('N')
                        moves.append(NightCheck.valid_moves(j, i, turn, board, in_check, king_loc))
                    elif board[i][j][0] == 'B':
                        # moves.append('B')
                        moves.append(BishopCheck.valid_moves(j, i, turn, board, in_check, king_loc))
                    elif board[i][j][0] == 'K':
                        # moves.append('K')
                        moves.append(KingCheck.valid_moves(j, i, turn, board, in_check, king_loc))
                    elif board[i][j][0] == 'Q':
                        # moves.append('Q')
                        moves.append(QueenCheck.valid_moves(j, i, turn, board, in_check, king_loc))
        moves = [x for xs in moves for x in xs]
        return moves
    return []


def labelled_all_possible_moves(turn, board, in_check, king_loc):  # for the colour which turn it is
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j][-1] == turn:
                if board[i][j][0] == 'P':
                    # moves.append('P')
                    if len(PawnCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            PawnCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
                elif board[i][j][0] == 'R':
                    # moves.append('R')
                    if len(RookCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            RookCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
                elif board[i][j][0] == 'N':
                    # moves.append('N')
                    if len(NightCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            NightCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
                elif board[i][j][0] == 'B':
                    # moves.append('B')
                    if len(BishopCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            BishopCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
                elif board[i][j][0] == 'K':
                    # moves.append('K')
                    if len(KingCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            KingCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
                elif board[i][j][0] == 'Q':
                    # moves.append('Q')
                    if len(QueenCheck.valid_moves(j, i, turn, board, in_check, king_loc)) != 0:
                        moves.append(
                            QueenCheck.valid_moves(j, i, turn, board, in_check, king_loc) + [[chr(j + 97), i + 1]])
    moves_labelled = []
    # put destination to move to at the start and where the piece was as the second value
    for piece_moves in moves:
        for loc in range(len(piece_moves) - 1):
            key = f'{chr(piece_moves[loc][1] + 97)}{piece_moves[loc][0] + 1}'
            moves_labelled.append([piece_moves[-1][0]+str(piece_moves[-1][1])+ key])
    return moves_labelled
