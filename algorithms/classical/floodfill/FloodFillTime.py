from algorithms.utilities import MoveMouse, Utils, Walls
from collections import deque
import numpy as np

class FloodFillTime(Walls, Utils, MoveMouse):

    def __init__(self, walls, maze_width=16, maze_height=16):
        self.start_memory = self.memory_usage()
        self.total_memory_used = 0
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.inf = self.maze_width * self.maze_height
        self.flood_map = [[self.inf for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        self.goalPositions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }
        self.u = 0
        self.s = 0.18
        self.s_stop = 0.09
        self.d = 0.03
        self.v_max = 3
        self.a = 0.5 * 9.81
        self.turn_time = np.sqrt((self.d * (np.pi/2)) / (2*self.a))
        self.tot_t = 0

    def get_acceleration_time(self, s):
        ceof = [0.5*self.a, self.u, -s]
        roots = np.roots(ceof)
        t = roots[roots > 0][0]
        return t

    def get_stop_time(self):
        if self.u == 0:
            return 0
        t = (2*self.s_stop)/self.u
        self.u = 0
        return t

    def get_turn_time(self, action, old_orientation):
        if action == (old_orientation + 2) % 4:
            return 0
        return np.sqrt((self.d * (np.pi/2)) / (2*self.a))

    def get_time_taken_for_action(self, action, old_orientation, curr_state):
        if action == old_orientation:
            t = self.get_acceleration_time(self.s)
            self.u = min(self.u + self.a * t, self.v_max)
        else:
            t_stop = self.get_stop_time()
            t_turn = self.get_turn_time(action, old_orientation)
            t_acc = self.get_acceleration_time(self.s_stop)
            t = t_stop + t_turn + t_acc
            self.u = min(self.u + self.a * t_acc, self.v_max)
        self.tot_t += t
        return t

    def flood_fill(self):
        queue = deque([(pos, self.orientation) for pos in self.goalPositions])
        visited = set(self.goalPositions)
        pos: tuple[int, int]
        for pos in self.goalPositions:
            self.flood_map[pos[0]][pos[1]] = 0

        while queue:
            (x, y), orientation = queue.popleft()
            current_time = self.flood_map[x][y]

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                    if not self.wall_between((x, y), direction):
                        time = self.get_time_taken_for_action(action=direction, old_orientation=orientation, curr_state=(x, y))
                        if self.flood_map[nx][ny] > current_time + time:
                            self.flood_map[nx][ny] = current_time + time
                            if (nx, ny) not in visited:
                                queue.append(((nx, ny), direction))
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
        return direction

    def get_path_from_flood_map(self):
        self.reset_env()
        self.flood_fill()
        self.path.append(self.start_position)
        while self.curr_position not in self.goalPositions:
            direction = self.choose_next_position()
            self.move_update_position(direction)

        end_memory = self.memory_usage()
        self.total_memory_used = end_memory - self.start_memory
        return self.path
