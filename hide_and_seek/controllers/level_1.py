import hide_and_seek.utils.constants as Constants


class Backtrack:
    def __init__(self, table, players):
        """Constructor
        table: .ui.table class
        view_range= {'hider': x, 'seeker': y}: view range of hider and seeker
        """
        self._table = table
        self._players = players

    def bfs(self, _x, _y, u, v, n, m):
        table = self._table.get_table()
        vis = [[-1 for i in range(m)] for j in range(n)]

        trace = [[[] for i in range(m)] for j in range(n)]

        queue = [[_x, _y]]
        vis[_x][_y] = 0
        trace[_x][_y] = [_x, _y]

        print(_x, _y, u, v)
        while len(queue) > 0:
            x, y = queue.pop(0)
            if x == u and y == v:
                path = [[u, v]]
                while u != _x or v != _y:
                    a, b = trace[u][v]
                    u, v = a, b
                    path.append([u, v])
                return path

            for direct in range(8):
                if self._table.moveable(x, y, direct):
                    a = x + Constants.directions[direct]["x"]
                    b = y + Constants.directions[direct]["y"]

                    if vis[a][b] == -1 and (table[a][b] != 1 and table[a][b] != 4):
                        vis[a][b] = vis[x][y] + 1
                        trace[a][b] = [x, y]
                        queue.append([a, b])
        return None

    def dfs(self, table, seeker_pos):
        stack = [[seeker_pos[0], seeker_pos[1]]]
        n = len(table)
        m = len(table[1])
        vis = [[-1 for i in range(m)] for j in range(n)]
        trace = stack
        vis[seeker_pos[0]][seeker_pos[1]] = 1

        while len(stack) > 0:
            tmp = stack.pop()
            x, y = tmp[0], tmp[1]

            for i in range(1, len(self._players)):
                if (
                    abs(self._players[i][0] - x) <= seeker_pos[2]
                    and abs(self._players[i][1] - y) <= seeker_pos[2]
                ):
                    path = self.bfs(
                        x, y, self._players[i][0], self._players[i][1], n, m
                    )
                    if path is None:
                        raise Exception(
                            "Path return none between {},{} and {},{}".format(
                                x, y, self._players[i][0], self._players[i][1]
                            )
                        )
                    path.reverse()
                    for it in path:
                        vis[it[0]][it[1]] = 1
                    for i in range(len(path)):
                        trace.append(path[i])
                        for direct in range(8):
                            if self._table.moveable(x, y, direct):

                                u = x + Constants.directions[direct]["x"]
                                v = y + Constants.directions[direct]["y"]
                                if i < len(path) - 1:
                                    if (
                                        u != path[i + 1][0]
                                        or v != path[i + 1][1]
                                        and vis[u][v] == -1
                                    ):
                                        stack.append([u, v])
                                        vis[u][v] = 1

                    break

            for direct in range(8):
                if direct % 2 == 0:
                    continue
                if self._table.moveable(x, y, direct):
                    u = x + Constants.directions[direct]["x"]
                    v = y + Constants.directions[direct]["y"]

                    if vis[u][v] == -1:
                        trace.append([u, v])
                        vis[u][v] = 1
        return trace

    def run(self):
        trace = []  # self.dfs(self._table.get_table(), self._players[0])
        return trace
