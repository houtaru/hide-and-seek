import pygame
from pygame.locals import Rect

import hide_and_seek.utils.constants as Constants


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, rect, color, radius, view_range, moveable, pushable):
        pygame.sprite.Sprite.__init__(self)
        self._pos = {"y": x, "x": y}
        self._rect = rect
        self._color = color
        self._radius = radius
        self._view_range = view_range
        self._movable = moveable
        self._pushable = pushable

    def __str__(self):
        return "At ({}, {}) with color {}, view range: {}, moveable: {}, pushable: {}".format(
            self._pos["x"],
            self._pos["y"],
            self._color,
            self._view_range,
            self._movable,
            self._pushable,
        )

    def move(self, direct, delta, scr_rect):
        """
        Parameters:
            direct: 0 -> 7
            delta={"x": 0, "y": 0} : dictionary stores movement distance of player
            scr_rect=Rect(0, 0, opt["screen_width"], opt["screen_height"]) : largest rect display on GUI
        """
        if not self._movable:
            return
        self._pos["x"] += Constants.directions[direct]["x"]
        self._pos["y"] += Constants.directions[direct]["y"]

        self._rect.move_ip(delta["x"], delta["y"])
        self._rect.clamp(scr_rect)

    def draw(self, window, n, m, grid_size):
        view_area = {
            "x": max(0, self._pos["x"] - self._view_range),
            "y": max(0, self._pos["y"] - self._view_range),
            "u": min(n - 1, self._pos["x"] + self._view_range),
            "v": min(m - 1, self._pos["y"] + self._view_range),
        }
        view_rect = Rect(
            max(1, self._rect.x - grid_size["x"] * self._view_range),
            max(1, self._rect.y - grid_size["y"] * self._view_range),
            grid_size["x"] * (view_area["u"] - view_area["x"] + 1),
            grid_size["y"] * (view_area["v"] - view_area["y"] + 1),
        )
        pygame.draw.rect(
            window, Constants.colors["blur_{}".format(self._color)], view_rect
        )

        pygame.draw.circle(
            window, Constants.colors[self._color], self._rect.center, self._radius, 0
        )
