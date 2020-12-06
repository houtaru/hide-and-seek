from pygame.locals import Rect

screen_rect = Rect(0, 0, opt["screen_width"], opt["screen_height"])

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "blur_red": (255, 135, 133),
    "green": (0, 255, 0),
    "gray": (133, 133, 133),
    "blue": (0, 0, 255),
    "blur_blue": (133, 135, 255),
    "yellow": (255, 255, 0),
}

directions = [
    {"x": -1, "y": -1},
    {"x": -1, "y": 0},
    {"x": -1, "y": 1},
    {"x": 0, "y": 1},
    {"x": 1, "y": 1},
    {"x": 1, "y": 0},
    {"x": 1, "y": -1},
    {"x": 0, "y": -1},
]
