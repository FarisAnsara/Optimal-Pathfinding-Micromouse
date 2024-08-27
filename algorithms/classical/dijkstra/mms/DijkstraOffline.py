import heapq
import os
import sys
import time
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from algorithms.classical.floodfill.mms.FloodFillOnline import FloodFillOnline
from algorithms.mms_integration import API

class DijkstraOffline(FloodFillOnline):
    def __init__(self):
        super().__init__()
        self.distances = [[float('inf')] * self.mazeWidth for _ in range(self.mazeHeight)]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,  # Moving North
            (1, 0): self.EAST,  # Moving East
            (0, -1): self.SOUTH,  # Moving South
            (-1, 0): self.WEST  # Moving West
        }
        self.path = []
        self.goal_positions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]

    def dijkstra(self):
        pq = [(0, self.start_position)]
        self.distances[self.start_position[0]][self.start_position[1]] = 0
        while pq:
            current_distance, position = heapq.heappop(pq)
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
                        heapq.heappush(pq, (new_distance, neighbor))

    def find_shortest_path_to_goal(self):
        self.dijkstra()
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

    def update_text_dijkstra(self):
        for y in range(self.mazeHeight):
            for x in range(self.mazeWidth):
                if self.distances[y][x] != float('inf'):
                    API.setText(x, y, self.distances[y][x])


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


dijkstra = DijkstraOffline()
dijkstra.move_and_floodfill()
dijkstra.go_back_to_start()
API.clearAllColor()
API.clearAllText()
dijkstra.dijkstra()
dijkstra.update_text_dijkstra()
time.sleep(2)
dijkstra.take_shortest_path()
time.sleep(2)
dijkstra.reset_env()
dijkstra.move_along_shortest_path()