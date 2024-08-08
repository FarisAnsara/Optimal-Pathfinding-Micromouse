import sys
import os
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from algorithms.mms_integration import MoveMouse, Walls, Utils, API


class FloodFillOnline(MoveMouse, Walls, Utils):

    def __init__(self, maze_width=16, maze_height=16):
        MoveMouse.__init__(self)
        Walls.__init__(self, maze_width, maze_height)
        Utils.__init__(self)
        self.mazeWidth = maze_width
        self.mazeHeight = maze_height
        inf = 100000
        self.flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        self.found_shortest = False
        self.goal_position = None

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

    def move_and_floodfill(self, ensure_shortest=True):
        while not self.found_shortest:
            self.update_walls(position=self.curr_position, orientation=self.orientation)
            self.update_text_flood_map(self.flood_map)
            neighbors_desc = self.find_neighbor_descending()
            if self.is_goal_position(self.curr_position):
                self.found_shortest = True
                break

            if not neighbors_desc:
                self.flood_map = self.flood_fill(self.get_goal_position())  # Use the returned flood map

                self.move_and_floodfill()

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            self.move(directions)
            if not self.goal_position and self.curr_position in self.get_goal_position():
                self.goal_position = self.curr_position

        if ensure_shortest:
            self.ensure_shortest_path()

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
        self.update_text_flood_map(self.flood_map)

    def move_to_position(self, position, go_back_start=False, take_shortest_path=False):
        while not self.curr_position == position:
            current_x, current_y = self.curr_position

            if take_shortest_path:
                API.setColor(current_x, current_y, 'r')

            flood_map = self.flood_fill(position)
            self.update_walls(position=self.curr_position, orientation=self.orientation)
            neighbors_desc = self.find_neighbor_descending(flood_map)

            if not neighbors_desc:
                break

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            self.move(directions)

    def go_back_to_start(self):
        self.move_to_position(self.start_position, go_back_start=True)

    def take_shortest_path(self):
        self.move_and_floodfill()

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

    def take_shortest_path(self):
        self.move_to_position(self.goal_position, take_shortest_path=True)


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running floodfill algorithm...")
    exp = FloodFillOnline()
    exp.move_and_floodfill()
    exp.reset_env()
    exp.take_shortest_path()


if __name__ == "__main__":
    main()
