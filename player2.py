from __future__ import annotations
from itertools import combinations
from consts import Board, Color, Edge, NUM_NODES


class Player2:

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        moves = []

        for i in range(NUM_NODES):
            for j in range(i + 1, NUM_NODES):
                if board[i][j] != Color.UNCOLORED:
                    continue

                allowed = True

                for k in range(NUM_NODES):
                    if k == i or k == j:
                        continue

                    if (board[i][k] == player and
                            board[j][k] == player):
                        allowed = False
                        break

                if allowed:
                    moves.append((i, j))

        return moves

    @staticmethod
    def get_maximal_allowed_sets(
        player: Color, board: Board
    ) -> set[frozenset[Edge]]:

        moves = Player2.get_allowed_moves(player, board)
        maximal_sets = set()

        # Search from largest to smallest.
        for size in range(len(moves), -1, -1):
            for subset in combinations(moves, size):
                chosen = set(subset)
                valid = True

                for a, b, c in combinations(range(NUM_NODES), 3):
                    triangle = [(a, b), (a, c), (b, c)]

                    if all(
                        board[i][j] == player or
                        (i, j) in chosen
                        for i, j in triangle
                    ):
                        valid = False
                        break

                if valid:
                    maximal_sets.add(frozenset(subset))

            if maximal_sets:
                return maximal_sets

        return {frozenset()}

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        required_nodes = set()

        for i in range(NUM_NODES):
            for j in range(i + 1, NUM_NODES):
                if board[i][j] in (Color.P1, Color.P2):
                    required_nodes.add(i)
                    required_nodes.add(j)

        # Try the smallest node subsets first.
        for size in range(max(2, len(required_nodes)),
                          NUM_NODES + 1):
            for nodes in combinations(range(NUM_NODES), size):
                nodes = set(nodes)

                if not required_nodes.issubset(nodes):
                    continue

                # The miniboard must be complete.
                if any(
                    board[i][j] == Color.NONE
                    for i, j in combinations(sorted(nodes), 2)
                ):
                    continue

                mini = [
                    [Color.NONE for _ in range(NUM_NODES)]
                    for _ in range(NUM_NODES)
                ]

                for i, j in combinations(sorted(nodes), 2):
                    mini[i][j] = board[i][j]
                    mini[j][i] = board[j][i]

                if Player2.get_allowed_moves(Color.P2, mini):
                    return mini

        return None

    @staticmethod
    def get_move(board: Board) -> Edge:
        mini = Player2.get_miniboard(board)

        if mini is None:
            raise ValueError("No valid miniboard found")

        moves = Player2.get_allowed_moves(Color.P2, mini)

        if len(moves) == 1:
            return moves[0]

        # Count appearances in maximum P2-allowed sets.
        p2_sets = Player2.get_maximal_allowed_sets(Color.P2, mini)

        p2_counts = {
            move: sum(move in s for s in p2_sets)
            for move in moves
        }

        max_count = max(p2_counts.values())
        candidates = [
            move for move in moves
            if p2_counts[move] == max_count
        ]

        if len(candidates) == 1:
            return candidates[0]

        # Break ties using maximum P1-allowed sets.
        p1_sets = Player2.get_maximal_allowed_sets(Color.P1, mini)

        p1_counts = {
            move: sum(move in s for s in p1_sets)
            for move in candidates
        }

        return max(candidates, key=lambda move: p1_counts[move])
