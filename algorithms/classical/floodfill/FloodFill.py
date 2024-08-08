from typing import List, Tuple

from algorithms.utilities import MoveMouse, Utils, Walls
from collections import deque


class FloodFill(Walls, Utils, MoveMouse):

    def __init__(self, walls, maze_width=16, maze_height=16):
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.inf = self.maze_width * self.maze_height
        self.flood_map = [[self.inf for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        self.found_shortest = False
        self.goalPositions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]

    def flood_fill(self):
        queue = deque(self.goalPositions)
        visited = set(self.goalPositions)
        pos: tuple[int, int]
        for pos in self.goalPositions:
            self.flood_map[pos[0]][pos[1]] = 0

        while queue:
            x, y = queue.popleft()
            current_distance = self.flood_map[x][y]

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                    if not self.wall_between((x, y), direction) and self.flood_map[nx][ny] > current_distance + 1:
                        self.flood_map[nx][ny] = current_distance + 1
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))
                            visited.add((nx, ny))

    def find_neighbors_descending(self):
        x, y = self.curr_position
        current_value = self.flood_map[x][y]
        neighbors = []
        for direction in self.directions:
            dx, dy = self.directionVectors[direction]
            nx, ny = self.curr_position[0] + dx, self.curr_position[1] + dy
            if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                neighbor_value = self.flood_map[nx][ny]
                if neighbor_value < current_value and not self.wall_between(self.curr_position, direction):
                    neighbors.append((direction, neighbor_value))

        neighbors.sort(key=lambda x: x[1])
        return neighbors

    def choose_next_position(self):
        neighbors = self.find_neighbors_descending()
        directions = [neighbors[i][0] for i in range(len(neighbors))]
        direction = directions[0]
        x, y = self.curr_position
        dx, dy = self.directionVectors[direction]
        neighbor = (x + dx, y + dy)
        if len(directions) == 1:
            return direction, neighbor

        for val in directions:
            if val <= direction == self.orientation:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)
                return val, neighbor

        return direction, neighbor

    def get_path_from_flood_map(self):
        self.reset_env()
        self.flood_fill()
        while self.curr_position not in self.goalPositions:
            direction, next_position = self.choose_next_position()
            self.move_update_position(direction)

        return self.path