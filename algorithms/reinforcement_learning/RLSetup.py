import sys

from algorithms.utilities import MoveMouse, Utils, Walls
import numpy as np
import random
from algorithms.utilities.Stats import Stats


class RLSetup(MoveMouse, Walls, Utils):
    def __init__(self, walls, maze_width=16, maze_height=16, epsilon=0.99, num_agents=15):
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.q_table = np.zeros((16, 16, 4))
        self.goal_positions = self.get_goal_position()
        self.goal_reward = 1000
        self.unfeasable_path_reward = -10000
        self.unfeasable_paths = []
        self.dead_ends = []
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1),
            self.EAST: (1, 0),
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }
        self.epsilon = epsilon
        self.u = 0
        self.s = 0.18
        self.s_stop = 0.09
        self.d = 0.03
        self.v_max = 1
        self.a = 0.5
        self.time_cache = {}
        self.episode = 0
        self.accumalated_reward = 0
        self.previous_reward = 0
        self.threshold = 1
        self.threshold_discount = 0.1
        self.min_threshold = 0.01
        self.num_agents = num_agents

    def get_acceleration_time(self, s):
        ceof = [0.5*self.a, self.u, -s]
        roots = np.roots(ceof)
        t = roots[roots > 0][0]
        return t

    def get_stop_time(self):
        t = (2*self.s_stop)/self.u
        self.u = 0
        return t

    def get_turn_time(self, action, old_orientation):
        if action == (old_orientation + 2) % 4:
            return 0
        return 0.2170803763674803

    def get_time_taken_for_action(self, action, old_orientation, curr_state):
        cache_key = (curr_state, action, old_orientation)
        if cache_key in self.time_cache:
            t = self.time_cache[cache_key]
            if action != old_orientation:
                self.u = 0
            self.u = min(self.u + self.a * t, self.v_max)
            return t
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

    def get_possible_actions_next_states(self, position, unfeas=False):
        actions_next_states = []
        if self.is_dead_end(position) and self.wall_between(position, self.orientation):
            self.dead_ends.append(position)
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                if not self.wall_between(position, direction):
                    action = direction
            dx, dy = self.directionVectors[action]
            next_state = (position[0] + dx, position[1] + dy)
            return [(action, next_state)]

        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = position[0] + dx, position[1] + dy
            if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                neighbor_value = (nx, ny)
                if not self.wall_between(position, direction) and (direction, position) not in self.unfeasable_paths:
                    if unfeas or (direction + 2) % 4 != self.orientation:
                        actions_next_states.append((direction, neighbor_value))
                else:
                    self.q_table[position[0]][position[1]][direction] = -100000
            else:
                if nx < 0:
                    self.q_table[position[0]][position[1]][3] = -100000
                if nx > 15:
                    self.q_table[position[0]][position[1]][1] = -100000
                if ny < 0:
                    self.q_table[position[0]][position[1]][2] = -100000
                if ny > 15:
                    self.q_table[position[0]][position[1]][0] = -100000
        return actions_next_states

    def is_dead_end(self, position):
        return sum(self.walls[position]) == 3

    def choose_action(self, state):
        actions_next_states = self.get_possible_actions_next_states(state)
        if len(actions_next_states) == 1:
            return actions_next_states[0][0]
        if random.random() < self.epsilon:
            return random.choice(actions_next_states)[0]
        else:
            q_values = self.q_table[state[0], state[1], :]
            best_action = max(actions_next_states, key=lambda x: q_values[x[0]])[0]
            return best_action

    def get_reward(self, next_state, action, old_orientation, curr_state, dynaq=False):
        if self.threshold == self.min_threshold:
            self.path.append(next_state)

        if next_state in self.goal_positions:
            return self.goal_reward
        elif self.is_dead_end(next_state):
            return self.unfeasable_path_reward
        else:
            if not dynaq:
                return -0.25
            return -self.get_time_taken_for_action(action, old_orientation, curr_state)

    def get_max_q_values(self):
        max_q_val = [[0 for _ in range(16)] for _ in range(16)]
        for i in range(self.q_table.shape[0]):
            for j in range(self.q_table.shape[1]):
                max_val = np.max(self.q_table[i, j])
                max_q_val[i][j] = int(max_val)
        return max_q_val


    def early_stopping(self):
        if abs(self.accumalated_reward - self.previous_reward) < self.threshold:
            if self.threshold <= self.min_threshold:
                return True
            self.threshold = self.threshold * self.threshold_discount
            return False
        self.threshold = 1
        return False

    def get_time_from_path(self):
        stats = Stats()
        return stats.get_time_from_path(self.get_path())

