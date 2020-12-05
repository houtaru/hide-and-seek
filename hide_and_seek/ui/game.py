import os
import pygame
from pygame.locals import Rect


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, rect, color, radius, moveable, pushable):
        pygame.sprite.Sprite.__init__(self)
        self._pos = {"x": x, "y": y}
        self._rect = rect
        self._color = color
        self._radius = radius
        self._movable = moveable
        self._pushable = pushable

    def move(self, delta={"x": 0, "y": 0}):
        if not self._movable:
            return
        self._rect.move_ip(delta["x"], delta["y"])
        self._rect.clamp(SCREEN_RECT)

    def draw(self, window):
        pygame.draw.circle(window, self._color, self._rect.center, self._radius, 0)


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

        self._colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "gray": (133, 133, 133),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
        }

        self._directions = [
            {"x": -1, "y": -1},
            {"x": -1, "y": 0},
            {"x": -1, "y": 1},
            {"x": 0, "y": 1},
            {"x": 1, "y": 1},
            {"x": 1, "y": 0},
            {"x": 1, "y": -1},
            {"x": 0, "y": -1},
        ]

    def draw(self, window, scr_rect):
        pygame.draw.rect(window, self._colors["white"], scr_rect)

        self.draw_grids(window)
        self.draw_table(window)

    def draw_grids(self, window):
        for i in range(self._n):
            for j in range(self._m):
                print(self._table[i][j], end=" ")
            print("\n")
        for i in range(self._n):
            for j in range(self._m):
                lhs = (
                    self._start["x"] + j * self._grid_size["x"],
                    self._start["y"] + i * self._grid_size["y"],
                )
                rhs = (
                    self._start["x"] + (j + 1) * self._grid_size["x"],
                    self._start["y"] + (i + 1) * self._grid_size["y"],
                )

                cur_color = self._colors["white"]
                if self._table[i][j] == 1:  # Wall
                    cur_color = self._colors["gray"]
                if self._table[i][j] == 4:  # Obstacle
                    cur_color = self._colors["yellow"]
                # print(i, j, lhs, rhs, cur_color)
                pygame.draw.rect(
                    window, cur_color, Rect(lhs[0], lhs[1], rhs[0], rhs[1])
                )

    def draw_table(self, window):
        for i in range(self._n + 1):
            hla = self._start["x"] + i * self._grid_size["x"]
            vla = self._start["y"] + i * self._grid_size["y"]
            # draw horizontal line
            pygame.draw.line(
                window,
                self._colors["black"],
                (hla, self._start["y"]),
                (hla, self._start["y"] + self._n * self._grid_size["y"]),
                self._line_thickness,
            )
            # draw vertical line
            pygame.draw.line(
                window,
                self._colors["black"],
                (self._start["x"], vla),
                (self._start["x"] + self._n * self._grid_size["x"], vla),
                self._line_thickness,
            )

    def moveable(self, x, y, direct):
        dx, dy = elf._directions[direct]["x"], self._directions[direct]["y"]
        u, v = x + dx, y + dy
        if self._table[u][v] == 0:
            if directions % 2 == 0:
                return self._table[u][y] == 0 or self._table[x][v] == 0
            return True
        return False

    def get_board_pos(self, x, y):
        return [
            self._start["x"] + (x - 1) * self._grid_size,
            self._start["x"] + (y - 1) * self._grid_size,
        ]


class Game:
    def __init__(self, opt):
        pygame.init()
        pygame.display.set_caption("Hide and Seek")
        self.window = pygame.display.set_mode(
            (opt["screen_width"], opt["screen_height"])
        )
        self.fps = opt["FRAME_PER_SECONDS"]
        self.rect = Rect(0, 0, opt["screen_width"], opt["screen_height"])
        self.table = Table(
            opt["map"],
            {"scr_wt": opt["screen_height"], "scr_ht": opt["screen_height"]},
            opt["line"]["thickness"],
        )

    def __del__(self):
        pygame.quit()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        self.draw()
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # agent
            # self.draw()

    def draw(self):
        self.table.draw(self.window, self.rect)
        pygame.display.update()
