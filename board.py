SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    sr, sc = start
    er, ec = end

    # Move the piece
    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."

    # If this is a capture, remove the jumped piece
    if abs(er - sr) == 2 and abs(ec - sc) == 2:
        mr = (sr + er) // 2
        mc = (sc + ec) // 2
        board[mr][mc] = "."
