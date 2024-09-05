import os
import sys
import time
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '', '..', '..', '..')))
from MMS.classical.floodfill.FloodFillOnline import FloodFillOnline
from MMS.mms_integration import API


class BFSOffline(FloodFillOnline):
    def __init__(self):
        super().__init__()
        self.distances = [[float('inf')] * self.mazeWidth for _ in range(self.mazeHeight)]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }

    def run_bfs(self):
        queue = deque([self.start_position])
        x, y = self.start_position
        self.distances[y][x] = 0
        visited = set()

        while queue:
            position = queue.pop()
            visited.add(position)
            x, y = position

            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)

                if (0 <= neighbor[0] < self.mazeWidth and 0 <= neighbor[1] < self.mazeHeight
                        and not self.wall_between(position, direction) and neighbor not in visited):
                    queue.appendleft(neighbor)
                    nx, ny = neighbor
                    self.distances[ny][nx] = self.distances[y][x] + 1
                    API.setColor(nx, ny, 'b')

    def find_shortest_path_to_goal(self):
        goal_position = min(self.get_goal_position(), key=lambda pos: self.distances[pos[1]][pos[0]])

        path = []
        current_position = goal_position
        while current_position != self.start_position:
            path.append(current_position)
            x, y = current_position
            neighbors = [(x + dx, y + dy) for dx, dy in self.directionVectors.values()]

            valid_neighbors = [
                pos for pos in neighbors
                if 0 <= pos[0] < self.mazeWidth and 0 <= pos[1] < self.mazeHeight and
                   not self.wall_between(current_position, self.directionVectors_inverse[(pos[0] - x, pos[1] - y)])
            ]

            current_position = min(valid_neighbors, key=lambda pos: self.distances[pos[1]][pos[0]])

        path.reverse()
        return path

    def move_along_shortest_path(self):
        path = self.find_shortest_path_to_goal()
        prev_pos = self.start_position
        for pos in path:
            API.setColor(pos[0], pos[1], 'g')
            direction = self.directionVectors_inverse[(pos[0] - prev_pos[0], pos[1] - prev_pos[1])]
            self.move_update_position(direction)
            prev_pos = pos

    def update_text_BFS(self):
        for y in range(self.mazeHeight):
            for x in range(self.mazeWidth):
                if self.distances[y][x] != float('inf'):
                    API.setText(x, y, self.distances[y][x])


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


bfs = BFSOffline()
bfs.move_and_floodfill()
bfs.go_back_to_start()
API.clearAllColor()
API.clearAllText()
bfs.run_bfs()
bfs.update_text_BFS()
time.sleep(2)
bfs.take_shortest_path()
time.sleep(2)
bfs.reset_env()
bfs.move_along_shortest_path()
