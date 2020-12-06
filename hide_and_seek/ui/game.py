import os
import pygame
from pygame.locals import Rect

from ..ui.player import Player
from ..controllers.tracker import Tracker
from ..ui.table import Table
import hide_and_seek.utils.constants as Constants


class Game:
    def __init__(self, opt):
        pygame.init()
        pygame.display.set_caption("Hide and Seek")
        self.window = pygame.display.set_mode(
            (opt["screen_width"], opt["screen_height"])
        )
        self.fps = opt["FRAME_PER_SECONDS"]
        self.rect = Constants.screen_rect
        self.table = Table(
            opt["map"],
            {"scr_wt": opt["screen_height"], "scr_ht": opt["screen_height"]},
            opt["line"]["thickness"],
        )

        _players = {"hider": [], "seeker": []}
        tmp_table = self.table.get_table()
        for i in range(len(tmp_table)):
            for j in range(len(tmp_table[i])):
                lhs = self.table.get_pos_on_board(i, j)
                if tmp_table[i][j] == 2:
                    _players["hider"].append(
                        Player(
                            x=i,
                            y=j,
                            rect=Rect(
                                lhs[0] + 1,
                                lhs[1] + 1,
                                self.table._grid_size["x"],
                                self.table._grid_size["y"],
                            ),
                            color="blue",
                            radius=self.table._grid_size["x"] / 3,
                            view_range=opt["view"]["hider"],
                            moveable=opt["moveable"]["hider"],
                            pushable=opt["pushable"]["hider"],
                        )
                    )
                if tmp_table[i][j] == 3:
                    _players["seeker"].append(
                        Player(
                            x=i,
                            y=j,
                            rect=Rect(
                                lhs[0] + 1,
                                lhs[1] + 1,
                                self.table._grid_size["x"],
                                self.table._grid_size["y"],
                            ),
                            color="red",
                            radius=self.table._grid_size["x"] / 3,
                            view_range=opt["view"]["seeker"],
                            moveable=opt["moveable"]["seeker"],
                            pushable=opt["pushable"]["seeker"],
                        )
                    )
        self.tracker = Tracker(_players)

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
        pygame.draw.rect(self.window, Constants.colors["white"], self.rect)
        self.tracker.draw(self.window, self.table.get_table(), self.table._grid_size)
        self.table.draw(self.window)
        pygame.display.update()
