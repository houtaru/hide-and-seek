import os
import pygame
from pygame.locals import Rect

from ..ui.player import Player
from ..ui.table import Table
import hide_and_seek.utils.constants as Constants
from ..utils.rand import Rand

from ..controllers.level_1 import Backtrack


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

        _players = {"hider": [], "seeker": []}
        temp = []
        for i in range(opt["amount"]["seeker"]):
            x, y = Rand().get_pos(self.table.get_table())
            self.table.update_table(x, y, 3)
            temp.append([0, 0, 3])
        for i in range(opt["amount"]["hider"]):
            x, y = Rand().get_pos(self.table.get_table())
            self.table.update_table(x, y, 2)
            temp.append([x, y, 2])

        for i, j, typ in temp:
            lhs = self.table.get_pos_on_board(i, j)
            if typ == 2:
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
            if typ == 3:
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
        self._players = _players
        self._list_player = temp

        self._result = Backtrack(self.table, self._list_player).run()
        print(self._result)

    def __del__(self):
        pygame.quit()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # agent
            self.draw()

    def draw_players(self):
        for type in ["hider", "seeker"]:
            for player in self._players[type]:
                player.draw(
                    self.window, self.table._n, self.table._m, self.table._grid_size
                )

    def draw(self):
        pygame.draw.rect(self.window, Constants.colors["white"], self.rect)
        self.draw_players()
        self.table.draw(self.window)
        pygame.display.update()
