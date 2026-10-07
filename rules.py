SIZE = 8


def simple_move(board, player, start, end):
        sr, sc = start
        er, ec = end

        piece = board[sr][sc]

        if piece == player + "K":
         return (
            board[er][ec] == "." and
            abs(er - sr) == 1 and
            abs(ec - sc) == 1
        )

        direction = -1 if player == "R" else 1

        return (
        board[er][ec] == "." and
        abs(er - sr) == 1 and
        abs(ec - sc) == 1 and
        er - sr == direction
    )


def capture_move(board, player, start, end):
        sr, sc = start
        er, ec = end

        piece = board[sr][sc]

        mr, mc = (sr + er) // 2, (sc + ec) // 2

        if board[er][ec] != ".":
            return False

        if abs(er - sr) != 2 or abs(ec - sc) != 2:
            return False

        if board[mr][mc] in (".", player, player + "K"):
            return False

        if piece == player + "K":
            return True

        direction = -1 if player == "R" else 1

        return er - sr == 2 * direction

def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"

def has_legal_move(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] not in (player, player + "K"):
                continue

            start = (r, c)

            for dr in (-2, -1, 1, 2):
                for dc in (-2, -1, 1, 2):
                    end = (r + dr, c + dc)

                    if not (0 <= end[0] < SIZE and 0 <= end[1] < SIZE):
                        continue

                    if simple_move(board, player, start, end):
                        return True

                    if capture_move(board, player, start, end):
                        return True

    return False


def has_capture(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] not in (player, player + "K"):
                continue

            start = (r, c)

            for dr in (-2, 2):
                for dc in (-2, 2):
                    end = (r + dr, c + dc)

                    if not (0 <= end[0] < SIZE and 0 <= end[1] < SIZE):
                        continue

                    if capture_move(board, player, start, end):
                        return True

    return False

def has_capture_from(board, player, start):
    sr, sc = start

    for dr in (-2, 2):
        for dc in (-2, 2):
            end = (sr + dr, sc + dc)

            if not (0 <= end[0] < SIZE and 0 <= end[1] < SIZE):
                continue

            if capture_move(board, player, start, end):
                return True

    return False