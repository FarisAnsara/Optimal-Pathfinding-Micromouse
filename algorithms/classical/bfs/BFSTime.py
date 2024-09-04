from algorithms.utilities import MoveMouse, Utils, Walls
from collections import deque
from algorithms.utilities.Stats import Stats
import numpy as np

class BFSTime(Walls, Utils, MoveMouse):


    def __init__(self, walls, maze_width=16, maze_height=16):
        self.start_memory = self.memory_usage()
        self.total_memory_used = 0
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.times = [[float('inf')] * self.maze_width for _ in range(self.maze_height)]
        self.goal_positions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }
        self.tot_t = 0
        self.u = 0
        self.s = 0.18
        self.s_stop = 0.09
        self.d = 0.03
        self.v_max = 3
        self.a = 0.5 * 9.81
        self.turn_time = np.sqrt((self.d * (np.pi/2)) / (2*self.a))

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

    def bfs(self):
        queue = deque([(self.start_position, self.NORTH)])
        visited = set()
        self.times[self.start_position[0]][self.start_position[1]] = 0
        while queue:
            position, orientation = queue.pop()
            visited.add(position)
            x, y = position
            current_distance = self.times[x][y]

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)
                new_orientation = direction
                if (0 <= neighbor[0] < self.maze_width and 0 <= neighbor[1] < self.maze_height
                        and not self.wall_between(position, direction) and neighbor not in visited):
                    queue.appendleft((neighbor, new_orientation))
                    time = self.get_time_taken_for_action(action=new_orientation, old_orientation=orientation, curr_state=position)
                    self.times[neighbor[0]][neighbor[1]] = current_distance + time

    def find_shortest_path_to_goal(self):
        self.bfs()
        goal_position = min(self.get_goal_position(), key=lambda pos: self.times[pos[0]][pos[1]])
        self.curr_position = goal_position
        self.path.append(self.curr_position)
        x,y =self.curr_position
        for direction in self.directions:
            dx, dy = self.directionVectors[direction]
            nx, ny = x + dx, y + dy
            if not self.wall_between(self.curr_position, direction) and (nx,ny) not in self.goal_positions:
                self.orientation = direction

        while self.curr_position != self.start_position:
            x, y = self.curr_position
            neighbors = [(x + dx, y + dy) for dx, dy in self.directionVectors.values()]
            valid_neighbors = [
                pos for pos in neighbors
                if 0 <= pos[0] < self.maze_width and 0 <= pos[1] < self.maze_height and
                   not self.wall_between(self.curr_position, self.directionVectors_inverse[(pos[0] - x, pos[1] - y)])
            ]
            next_position = min(valid_neighbors, key=lambda pos: self.times[pos[0]][pos[1]])
            direction = self.directionVectors_inverse[(next_position[0] - x, next_position[1] - y)]
            self.move_update_position(direction)

        self.path.reverse()
        end_memory = self.memory_usage()
        self.total_memory_used = end_memory - self.start_memory
        return self.path


