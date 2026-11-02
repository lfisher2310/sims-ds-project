from __future__ import annotations
from itertools import combinations
from consts import Board, Color, Edge, NUM_NODES


class GameBoard:
    """
    Game board manager class. Encapsulates behaviors concerning the state of the board.
    """

    def __init__(self):
        self.board = [
            [
                Color.NONE if i == j else Color.UNCOLORED
                for j in range(NUM_NODES)
            ]
            for i in range(NUM_NODES)
        ]

    def color_edge(self, edge: Edge, color: Color) -> None:
        i, j = edge
        self.board[i][j] = color
        self.board[j][i] = color

    def get_winner(self) -> Color | None:
        for a, b, c in combinations(range(NUM_NODES), 3):
            edges = (
                self.board[a][b],
                self.board[a][c],
                self.board[b][c],
            )

            if all(edge == Color.P1 for edge in edges):
                return Color.P2

            if all(edge == Color.P2 for edge in edges):
                return Color.P1

        return None

    def __str__(self):
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string
