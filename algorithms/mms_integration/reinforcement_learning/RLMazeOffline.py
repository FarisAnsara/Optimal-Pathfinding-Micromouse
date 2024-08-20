import numpy as np
import sys
from algorithms.mms_integration import API
from algorithms.classical.floodfill.mms.FloodFillOnline import FloodFillOnline
import random
# import sys


class RLMazeOffline(FloodFillOnline):

    def __init__(self, epsilon = 0.99):
        super().__init__()
        self.actions_not_to_take = []
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
        self.epsilon = epsilon
        self.u = 0
        self.s = 0.18
        self.s_stop = 0.09
        self.d = 0.03
        self.v_max = 1
        self.a = 0.5
        self.tot_t = 0

    def get_acceleration_time(self, s):
        ceof = [0.5*self.a, self.u, -s]
        roots = np.roots(ceof)
        t = roots[roots > 0][0]
        return t

    def get_angle(self, action):
        if action == (self.orientation + 2) % 4:
            return 0
        return 0.5*np.pi

    def get_stop_time(self):
        return (2*self.s_stop)/self.u

    def get_turn_time(self, angle):
        return np.sqrt((self.d * angle) / (2*self.a))

    def get_time_taken_for_action(self, action):
        if action == self.orientation:
            t = self.get_acceleration_time(self.s)
            self.tot_t += t
            self.u = min(self.u + self.a*t, self.v_max)
            return t
        angle = self.get_angle(action)
        t_stop = self.get_stop_time()
        t_turn = self.get_turn_time(angle)
        t_acc = self.get_acceleration_time(self.s_stop)
        t = t_stop + t_turn + t_acc
        self.tot_t += t
        self.u = min(self.u + self.a * t, self.v_max)
        return t

    def get_dead_ends(self):
        for position in self.positions:
            if self.is_dead_end(position):
                self.dead_ends.append(position)
                API.setColor(position[0], position[1], 'b')

    def get_actions_leading_to_dead_ends(self):
        global position
        for dead_end in self.dead_ends:
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                if not self.wall_between(dead_end, direction):
                    dx, dy = self.directionVectors[direction]
                    position = dead_end[0] + dx, dead_end[1] + dy
                    dir_inv = (direction + 2) % 4
                    break

            self.get_path_leading(position, dir_inv)

    def get_path_leading(self, position, dir_inv):
        num_walls = 0
        for dir in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            if self.wall_between(position, dir):
                num_walls += 1
        if num_walls == 2:
            self.actions_not_to_take.append((position, dir_inv))
            # self.get_path_leading(position, )

    def get_unfeasable_paths(self, position, visited=None, recur=False):
        if not self.is_dead_end(position):
            if not recur:
                return

        if visited is None:
            visited = set()

        visited.add(position)
        if self.is_dead_end(position):
            action = (self.get_possible_actions_next_states(position, unfeas=True)[0][0] + 2) % 4
            API.setColor(position[0], position[1], 'b')

        actions_next_states = self.get_possible_actions_next_states(position, unfeas=True)
        for act_state in actions_next_states:
            state = act_state[1]
            if state not in visited:
                walls_true = [wall == True for wall in self.walls[state]]
                action = (act_state[0] + 2) % 4
                self.unfeasable_paths.append((action, state))
                if sum(walls_true) >= 2:
                    self.get_unfeasable_paths(state, visited, recur=True)
    def get_possible_actions_next_states(self, position, unfeas=False):
        actions_next_states = []
        if self.is_dead_end(position) and self.wall_between(position, self.orientation):
            # self.dead_ends.append(position)
            API.setColor(position[0], position[1], 'r')
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                if not self.wall_between(position, direction):
                    action = direction
            dx, dy = self.directionVectors[action]
            next_state = (position[0]+dx, position[1]+dy)
            return [(action, next_state)]

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
        if not actions_next_states:
            action = (self.orientation + 2) % 4
            dx, dy = self.directionVectors[action]
            next_state = self.curr_position[0] + dx, self.curr_position[1] + dy
            self.unfeasable_paths.append((self.orientation, next_state))
            return action
        print(actions_next_states)
        if len(actions_next_states) == 1:
            return actions_next_states[0][0]
        if random.random() < self.epsilon:
            return random.choice(actions_next_states)[0]
        else:
            q_values = self.q_table[state[0], state[1], :]
            best_action = max(actions_next_states, key=lambda x: q_values[x[0]])[0]
            return best_action

    def get_reward(self, next_state, action):
        if next_state in self.goal_positions:
            return self.goal_reward
        elif self.is_dead_end(next_state):
            return self.unfeasable_path_reward
        else:
            return -self.get_time_taken_for_action(action)

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


