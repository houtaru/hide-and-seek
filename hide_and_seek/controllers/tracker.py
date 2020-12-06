import pygame

import hide_and_seek.utils.constants as Constants


class Tracker:
    def __init__(self, players):
        """
        players: {'hider': [], 'seeker': []}
        """
        self._players = players

    def draw(self, window, table, grid_size):
        for type in ["hider", "seeker"]:
            for player in self._players[type]:
                player.move(
                    3,
                    {
                        "x": Constants.directions[3]["x"] * grid_size,
                        "y": Constants.directions[3]["y"] * grid_size,
                    },
                    Constants.screen_rect,
                )
                player.draw(window, len(table), len(table[0]), grid_size)
                print(player, player._rect)
