import random
from datetime import datetime


class Rand:
    def __init__(self):
        random.seed(datetime.now())

    def rand(self, l, r):
        return random.randint(l, r)

    def get_pos(self, table):
        n = len(table)
        m = len(table[0])
        x = self.rand(0, n - 1)
        y = self.rand(0, n - 1)
        while True:
            if table[x][y] == 0:
                break
            x = self.rand(0, n - 1)
            y = self.rand(0, n - 1)
        return [x, y]
