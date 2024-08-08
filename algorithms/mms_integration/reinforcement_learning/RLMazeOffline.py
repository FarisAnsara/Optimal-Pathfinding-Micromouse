import numpy as np
import sys
from algorithms.mms_integration import API
from algorithms.classical.floodfill.mms.FloodFillOnline import FloodFillOnline
import random
# import sys


class RLMazeOffline(FloodFillOnline):

    def __init__(self):
        super().__init__()
        self.q_table = np.zeros((16, 16, 4))
        self.goal_positions = self.get_goal_position()
        self.goal_reward = 1000
        self.unfeasable_path_reward = -1000
        self.unfeasable_paths = []
        self.dead_ends = []
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1),
            self.EAST: (1, 0),
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }

    def get_possible_actions_next_states(self, position, unfeas=False):
        actions_next_states = []
        if self.is_dead_end(position) and self.wall_between(position,self.orientation):
            self.dead_ends.append(position)
            API.setColor(position[0], position[1], 'r')
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                if not self.wall_between(position, direction):
                    action = direction
            dx, dy = self.directionVectors[action]
            next_state = (position[0]+dx, position[1]+dy)
            return [(action,next_state)]

        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = position[0] + dx, position[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
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

    def get_reward(self, next_state):
        if next_state in self.goal_positions:
            return self.goal_reward
        elif self.is_dead_end(next_state):
            return self.unfeasable_path_reward
        else:
            return -1

    def get_all_unfeasable(self):
        for state in self.positions:
            try:
                self.get_unfeasable_paths(state)
            except Exception as e:
                log(f'state: {state}, err: {e}')

    def update_q_vals_on_API(self):
        for i in range(self.q_table.shape[0]):
            for j in range(self.q_table.shape[1]):
                max_val = np.max(self.q_table[i, j])
                API.setText(i, j, str(round(max_val, 2)))



def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


