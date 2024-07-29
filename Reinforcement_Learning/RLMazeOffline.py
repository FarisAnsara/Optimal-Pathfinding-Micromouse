import numpy as np
from Utilities import API
from Classical_Algorithms import FloodFill
import random
import sys


class RLMazeOffline(FloodFill):

    def __init__(self):
        # MoveMouse.__init__(self)
        # FloodFill.__init__(self)
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
            # self.get_unfeasable_paths(position)
            self.dead_ends.append(position)
            API.setColor(position[0], position[1], 'r')
            action = (self.orientation + 2) % 4
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

    def get_unfeasable_paths(self, position, visited=None, recur=False):
        # TODO: Add actions and states, this was, we check the action and the state prev, if inside, we don't give it as one of the actions.

        if not self.is_dead_end(position):
            if not recur:
                return

        if visited is None:
            visited = set()

        # if position in visited:
        #     return

        visited.add(position)
        if self.is_dead_end(position):
            log(f'possible: {self.get_possible_actions_next_states(position)}')
            action = (self.get_possible_actions_next_states(position)[0][0] + 2) % 4
            # self.unfeasable_paths.append((action, position))
            API.setColor(position[0], position[1], 'r')

        actions_next_states = self.get_possible_actions_next_states(position)
        for act_state in actions_next_states:
            state = act_state[1]
            if state not in visited:
                walls_true = [wall == True for wall in self.walls[state]]
                # log(f'State = {state}, walls = {walls_true}')
                action = (act_state[0] + 2) % 4
                self.unfeasable_paths.append((action, state))
                API.setColor(state[0], state[1], 'r')
                if sum(walls_true) >= 2:  # Dead end or almost dead end

                    self.get_unfeasable_paths(state, visited, recur=True)

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


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


