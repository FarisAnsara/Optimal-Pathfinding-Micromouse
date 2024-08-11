from algorithms.utilities import MoveMouse, Utils, Walls
from collections import deque


class FloodFill(Walls, Utils, MoveMouse):

    def __init__(self, walls, maze_width=16, maze_height=16):
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.inf = self.maze_width * self.maze_height
        self.flood_map = [[self.inf for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        self.goalPositions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,  # Moving North
            (1, 0): self.EAST,  # Moving East
            (0, -1): self.SOUTH,  # Moving South
            (-1, 0): self.WEST  # Moving West
        }

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
        direction = neighbors[0][0]
        neighbor_value = neighbors[0][1]
        if len(neighbors) == 1:
            return direction

        for val in neighbors[1::]:
            if val[0] == self.orientation and val[1] <= neighbor_value:
                return val[0]

        return direction

    def get_path_from_flood_map(self):
        self.reset_env()
        self.flood_fill()
        self.path.append(self.start_position)
        while self.curr_position not in self.goalPositions:
            direction = self.choose_next_position()
            self.move_update_position(direction)

        return self.path