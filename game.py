from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_legal_move,
    has_capture,
    has_capture_from
)



class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()
            pieces = any(
        cell in (self.player, self.player + "K")
        for row in self.board
        for cell in row
               )

            if not pieces:
               winner = "B" if self.player == "R" else "R"
               print(f"{winner} wins!")
               return

            if not has_legal_move(self.board, self.player):
               winner = "B" if self.player == "R" else "R"
               print(f"{winner} wins — no legal moves.")
               return
     
            raw = input(f"{self.player}> ").strip().lower().split()
            if raw == ["q"]:
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue
            start, end = (sr, sc), (er, ec)

            # If any capture exists, only captures are allowed
            if has_capture(self.board, self.player):
                if not capture_move(self.board, self.player, start, end):
                    print("Capture is mandatory.")
                    continue

                moving_piece = self.board[sr][sc]
                move_piece(self.board, start, end)

                was_promoted = (
                    moving_piece == "R" and end[0] == 0
                ) or (
                    moving_piece == "B" and end[0] == SIZE - 1
                )

                promote(self.board)

                if was_promoted:
                    print(
                        f"{moving_piece} captured at "
                        f"({(sr + er) // 2},{(sc + ec) // 2}) "
                        f"and moved to ({er},{ec}), promoted to "
                        f"{self.board[er][ec]}."
                    )
                else:
                    print(
                        f"{moving_piece} captured at "
                        f"({(sr + er) // 2},{(sc + ec) // 2}) "
                        f"and moved to ({er},{ec})."
                    )

                # Continue capturing with the same piece
                while has_capture_from(self.board, self.player, end):
                    current = end

                    raw = input(
                        f"{self.player} must continue capture> "
                    ).strip().lower().split()

                    if raw == ["q"]:
                        return

                    if len(raw) != 2:
                        print("Enter destination row and column.")
                        continue

                    try:
                        er, ec = map(int, raw)
                    except ValueError:
                        print("Coordinates must be numbers.")
                        continue

                    if not (0 <= er < SIZE and 0 <= ec < SIZE):
                        print("Outside board.")
                        continue

                    next_end = (er, ec)

                    if not capture_move(
                        self.board,
                        self.player,
                        current,
                        next_end
                    ):
                        print("Invalid capture.")
                        continue

                    sr, sc = current
                    moving_piece = self.board[sr][sc]

                    move_piece(self.board, current, next_end)

                    was_promoted = (
                        moving_piece == "R" and next_end[0] == 0
                    ) or (
                        moving_piece == "B" and next_end[0] == SIZE - 1
                    )

                    promote(self.board)

                    if was_promoted:
                        print(
                            f"{moving_piece} captured at "
                            f"({(sr + er) // 2},{(sc + ec) // 2}) "
                            f"and moved to ({er},{ec}), "
                            f"promoted to {self.board[er][ec]}."
                        )
                    else:
                        print(
                            f"{moving_piece} captured at "
                            f"({(sr + er) // 2},{(sc + ec) // 2}) "
                            f"and moved to ({er},{ec})."
                        )

                    end = next_end

            # No capture exists, so a normal move is allowed
            elif simple_move(self.board, self.player, start, end):
                moving_piece = self.board[sr][sc]

                move_piece(self.board, start, end)

                was_promoted = (
                    moving_piece == "R" and end[0] == 0
                ) or (
                    moving_piece == "B" and end[0] == SIZE - 1
                )

                promote(self.board)

                if was_promoted:
                    print(
                        f"{moving_piece} moved from "
                        f"({sr},{sc}) to ({er},{ec}) "
                        f"and was promoted to {self.board[er][ec]}."
                    )
                else:
                    print(
                        f"{moving_piece} moved from "
                        f"({sr},{sc}) to ({er},{ec})."
                    )

            else:
                print("Invalid move.")
                continue

            self.player = "B" if self.player == "R" else "R"