import pygame
from pygame.locals import Rect


class Player(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.dx = [0, 1, 0, -1]
        self.dy = [-1, 0, 1, 0]
        self.radius = Constants.PLAYER_RADIUS
        self.rect = Rect(
            initial_x - self.radius,
            initial_y - self.radius,
            self.radius*2,
            self.radius*2
        )
        self.color = color

    def move(self, direction):
        self.rect.move_ip(self.dx[direction] * (self.radius*3) , self.dy[direction] * (self.radius*2 + 2))
        self.rect.clamp(Constants.SCREEN_RECT)
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.rect.center, self.radius, 0)

class Game:
    def __init__(self, opt):
        pygame.init()
        pygame.display.set_caption("Hide and Seek")
        self.window = pygame.display.set_mode((opt.scr_wt, opt.scr_ht))
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0)
        }

        self.players = []
        for i in range(opt['player']['hider']):
            self.players.append(Player())

    def __del__(self):
        pygame.quit()
        
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(Constants.FRAME_PER_SECONDS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # agent 
            self.draw()

    def draw(self):
        
        pygame.draw.rect(self.window, (255, 255, 255), self.rect)
        tmp = Player(17, 17, (255, 0, 0))
        tmp.move(1)
        tmp.draw(self.window)
        for i in range(1, Constants.WINDOW_WIDTH, 32):
            pygame.draw.line(self.window, (0, 0, 0), (i, 3), (i, Constants.WINDOW_HEIGHT - 3), 2)
        
        for i in range(1, Constants.WINDOW_HEIGHT, 32):
            pygame.draw.line(self.window, (0, 0, 0), (1, i), (Constants.WINDOW_WIDTH - 3, i), 2)
        
        pygame.display.update()

