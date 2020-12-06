import pygame
from pygame.locals import Rect

import hide_and_seek.utils.constants as Constants


class Table:
    def __init__(self, map_path, scr_size, line_thickness):
        self._n = 0
        self._m = 0
        self._table = []
        with open(map_path, "r") as fin:
            content = fin.readlines()
            self._n, self._m = map(int, content[0].strip().split())

            self._table = [
                list(map(int, content[i].strip().split()))
                for i in range(1, self._n + 1)
            ]

            # Add obstacles to table
            for obstable in content[self._n + 1 :]:
                x, y, u, v = list(map(int, obstable.strip().split()))
                for i in range(x, u + 1):
                    for j in range(y, v + 1):
                        self._table[i - 1][j - 1] = 4

        self._start = {"x": 1, "y": 1}
        self._line_thickness = line_thickness
        self._grid_size = {
            "x": (scr_size["scr_wt"] - 1 - self._line_thickness) // self._n,
            "y": (scr_size["scr_ht"] - 1 - self._line_thickness) // self._m,
        }

    def get_pos_on_board(self, dy, dx):
        return (
            self._start["x"] + dx * self._grid_size["x"],
            self._start["y"] + dy * self._grid_size["y"],
        )

    def get_table(self):
        return self._table

    def update_table(self, x, y, new_value):
        self._table[x][y] = new_value

    def draw(self, window):
        self.draw_grids(window)
        self.draw_table(window)

    def draw_grids(self, window):
        for i in range(self._n):
            for j in range(self._m):
                lhs = self.get_pos_on_board(i, j)

                cur_color = None
                if self._table[i][j] == 1:  # Wall
                    cur_color = Constants.colors["gray"]
                if self._table[i][j] == 4:  # Obstacle
                    cur_color = Constants.colors["yellow"]

                if cur_color is None:
                    continue
                pygame.draw.rect(
                    window,
                    cur_color,
                    Rect(lhs[0], lhs[1], self._grid_size["x"], self._grid_size["y"]),
                )

    def draw_table(self, window):
        for i in range(self._n + 1):
            hla = self._start["x"] + i * self._grid_size["x"]
            vla = self._start["y"] + i * self._grid_size["y"]
            # draw horizontal line
            pygame.draw.line(
                window,
                Constants.colors["black"],
                (hla, self._start["y"]),
                (hla, self._start["y"] + self._n * self._grid_size["y"]),
                self._line_thickness,
            )
            # draw vertical line
            pygame.draw.line(
                window,
                Constants.colors["black"],
                (self._start["x"], vla),
                (self._start["x"] + self._n * self._grid_size["x"], vla),
                self._line_thickness,
            )

    def moveable(self, x, y, direct):
        dx, dy = (
            Constants.directions[direct]["x"],
            Constants.directions[direct]["y"],
        )
        u, v = x + dx, y + dy

        # Check inside board
        if not (u >= 0 and u < self._n and v >= 0 and v < self._m):
            return False

        if self._table[u][v] not in [1, 4]:

            # Diagonal case
            if direct % 2 == 0:
                return (self._table[u][y]) or (self._table[x][v] not in [1, 4])

            # Nomal case
            return True
        return False
