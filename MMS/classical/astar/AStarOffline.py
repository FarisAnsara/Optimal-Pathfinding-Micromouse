import heapq
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '', '..', '..', '..')))

from MMS.classical.floodfill.FloodFillOnline import FloodFillOnline
from MMS.mms_integration import API


class AstarOffline(FloodFillOnline):
    def __init__(self):
        super().__init__()
        self.distances = [[float('inf')] * self.mazeWidth for _ in range(self.mazeHeight)]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }
        self.path = []
        self.goal_positions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]

    def heuristic(self, pos):
        gx, gy = self.goal_positions[0]
        return abs(pos[0] - gx) + abs(pos[1] - gy)

    def a_star(self):
        pq = [(self.heuristic(self.start_position), 0, self.start_position)]
        self.distances[self.start_position[0]][self.start_position[1]] = 0

        while pq:
            priority, current_distance, position = heapq.heappop(pq)
            x, y = position

            if current_distance > self.distances[x][y]:
                continue

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)

                if (0 <= neighbor[0] < self.mazeWidth and 0 <= neighbor[1] < self.mazeHeight
                        and not self.wall_between(position, direction)):
                    new_distance = current_distance + 1

                    if new_distance < self.distances[neighbor[0]][neighbor[1]]:
                        self.distances[neighbor[0]][neighbor[1]] = new_distance
                        priority = new_distance + self.heuristic(neighbor)
                        heapq.heappush(pq, (priority, new_distance, neighbor))

    def find_shortest_path_to_goal(self):
        self.a_star()
        goal_position = min(self.goal_positions, key=lambda pos: self.distances[pos[0]][pos[1]])
        self.curr_position = goal_position

        while self.curr_position != self.start_position:
            self.path.append(self.curr_position)
            x, y = self.curr_position
            neighbors = [(x + dx, y + dy) for dx, dy in self.directionVectors.values()]
            valid_neighbors = [
                pos for pos in neighbors
                if 0 <= pos[0] < self.mazeWidth and 0 <= pos[1] < self.mazeHeight and
                   not self.wall_between(self.curr_position, self.directionVectors_inverse[(pos[0] - x, pos[1] - y)])
            ]
            self.curr_position = min(valid_neighbors, key=lambda pos: self.distances[pos[0]][pos[1]])

        self.path.reverse()
        return self.path

    def move_along_shortest_path(self):
        path = self.find_shortest_path_to_goal()
        prev_pos = self.start_position
        for pos in path:
            API.setColor(pos[0], pos[1], 'g')
            direction = self.directionVectors_inverse[(pos[0] - prev_pos[0], pos[1] - prev_pos[1])]
            self.move_update_position(direction)
            prev_pos = pos

    def update_text_astar(self):
        for y in range(self.mazeHeight):
            for x in range(self.mazeWidth):
                if self.distances[y][x] != float('inf'):
                    API.setText(x, y, self.distances[y][x])


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


astar = AstarOffline()
astar.move_and_floodfill()
astar.go_back_to_start()
API.clearAllColor()
API.clearAllText()
astar.a_star()
astar.update_text_astar()
time.sleep(2)
astar.take_shortest_path()
time.sleep(2)
astar.reset_env()
astar.move_along_shortest_path()