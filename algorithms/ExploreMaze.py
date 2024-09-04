import random
from collections import deque

from algorithms.utilities.MoveMouse import MoveMouse
from algorithms.utilities.Utils import Utils


class ExploreMaze(MoveMouse, Utils):

    def __init__(self, maze, maze_width=16, maze_height=16):
        MoveMouse.__init__(self)
        Utils.__init__(self)
        self.mazeWidth = maze_width
        self.mazeHeight = maze_height
        self.positions = [(n, m) for n in range(self.mazeWidth) for m in range(self.mazeHeight)]
        self.walls = {a: [False, False, False, False] for a in self.positions}
        self.maze = maze
        inf = self.mazeWidth * self.mazeHeight
        self.flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        self.goal_position = self.get_goal_position()
        self.found_shortest = False
        self.visited_cells = {a: False for a in self.positions}
        self.stop_exploring = False
        self.path.append(self.start_position)

    def wall_between(self, position, direction):
        return self.walls[position][direction]

    def update_walls(self, position):
        if self.visited_cells[position]:
            return

        self.visited_cells[position] = True
        walls = self.get_maze_info(position)
        self.walls[position] = walls
        self.update_walls_neighbors(walls[0], walls[1], walls[2], walls[3], position)

    def find_neighbor_descending(self, flood_map=None):
        neighbors = []
        if not flood_map:
            flood_map = self.flood_map

        current_value = flood_map[self.curr_position[0]][self.curr_position[1]]
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = self.curr_position[0] + dx, self.curr_position[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = flood_map[nx][ny]
                if neighbor_value < current_value and not self.wall_between(self.curr_position, direction):
                    neighbors.append((direction, neighbor_value))

        neighbors.sort(key=lambda x: x[1])
        return neighbors

    def update_walls_neighbors(self, north, east, south, west, position):
        x, y = position

        neighbors = {
            self.NORTH: (x, y + 1),
            self.EAST: (x + 1, y),
            self.SOUTH: (x, y - 1),
            self.WEST: (x - 1, y)
        }

        if 0 <= neighbors[self.NORTH][0] < self.mazeWidth and 0 <= neighbors[self.NORTH][1] < self.mazeHeight:
            self.walls[neighbors[self.NORTH]][2] = north

        if 0 <= neighbors[self.EAST][0] < self.mazeWidth and 0 <= neighbors[self.EAST][1] < self.mazeHeight:
            self.walls[neighbors[self.EAST]][3] = east

        if 0 <= neighbors[self.SOUTH][0] < self.mazeWidth and 0 <= neighbors[self.SOUTH][1] < self.mazeHeight:
            self.walls[neighbors[self.SOUTH]][0] = south

        if 0 <= neighbors[self.WEST][0] < self.mazeWidth and 0 <= neighbors[self.WEST][1] < self.mazeHeight:
            self.walls[neighbors[self.WEST]][1] = west

    def get_maze_info(self, position):
        return self.maze[position]

    def get_walls(self):
        return self.walls

    def move_and_floodfill(self, goal_position=None, ensure_shortest=True):
        while not self.stop_exploring:
            self.update_walls(position=self.curr_position)
            self.flood_map = self.flood_fill(self.get_goal_position())
            neighbors_desc = self.find_neighbor_descending()
            if self.is_goal_position(self.curr_position):
                self.stop_exploring = True

            if not neighbors_desc:
                self.flood_map = self.flood_fill(self.get_goal_position())
                self.move_and_floodfill()

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            self.move(directions)

            if not self.goal_position and self.curr_position in self.get_goal_position():
                self.goal_position = self.curr_position

        if ensure_shortest:
            self.ensure_shortest_path()

    def move(self, directions):
        if self.orientation in directions:
            self.move_update_position(self.orientation)
        elif (self.orientation + 1) % 4 in directions:
            if (self.orientation - 1) % 4 in directions:
                rand_direction = random.choice([(self.orientation + 1) % 4, (self.orientation - 1) % 4])
                self.move_update_position(rand_direction)
            else:
                self.move_update_position((self.orientation + 1) % 4)
        elif (self.orientation - 1) % 4 in directions:
            self.move_update_position((self.orientation - 1) % 4)
        else:
            self.move_update_position((self.orientation + 2) % 4)

    def flood_fill(self, goal_positions):
        inf = self.mazeHeight * self.mazeWidth
        local_flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        queue = deque(tuple(goal_positions))
        visited = set(goal_positions)

        if isinstance(goal_positions, tuple):
            local_flood_map[goal_positions[0]][goal_positions[1]] = 0
        else:
            for pos in goal_positions:
                local_flood_map[pos[0]][pos[1]] = 0
        n = 1
        while queue:
            if isinstance(goal_positions, tuple) and n == 1:
                x = queue.popleft()
                y = queue.popleft()
                n = 2
            else:
                x, y = queue.popleft()

            current_distance = local_flood_map[x][y]

            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                    if not self.wall_between((x, y), direction) and local_flood_map[nx][ny] > current_distance + 1:
                        local_flood_map[nx][ny] = current_distance + 1
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))
                            visited.add((nx, ny))

        return local_flood_map

    def ensure_shortest_path(self):
        nearest_undiscovered = self.find_nearest_undiscovered()
        if nearest_undiscovered:
            self.move_to_position(nearest_undiscovered)
            self.move_and_floodfill()

        self.flood_map = self.flood_fill(self.get_goal_position())

    def move_to_position(self, position):
        while not self.curr_position == position:
            flood_map = self.flood_fill(position)
            self.update_walls(position=self.curr_position)
            neighbors_desc = self.find_neighbor_descending(flood_map)

            if not neighbors_desc:
                break

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            self.move(directions)

    def find_neighbors(self, position):
        neighbors = []
        x = position[0]
        y = position[1]
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbors.append(neighbor)

        return neighbors

    def find_nearest_undiscovered(self):
        queue = deque([self.curr_position])
        visited = {self.curr_position}

        while queue:
            x, y = queue.popleft()
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                    if neighbor not in visited:
                        if not self.visited_cells[neighbor]:
                            neighbors = self.find_neighbors(neighbor)
                            for val in neighbors:
                                if not self.visited_cells[val]:
                                    return neighbor

                        queue.append(neighbor)
                        visited.add(neighbor)
                        self.visited_cells[neighbor] = True
        return None
