import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Helper_Classes import API
from Helper_Classes.MoveMouse import MoveMouse
from Classical_Algorithms.Flood import FloodFill

import numpy as np
import random
import pickle
import json

class SARSAExplore(Explore):
    def __init__(self, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.999, max_episodes=100, min_epsilon=0.01):
        super().__init__()
        # self.walls = {(0, 0): [False, True, True, True], (0, 1): [False, True, False, True], (0, 2): [True, False, False, True], (0, 3): [False, True, True, True], (0, 4): [False, False, False, True], (0, 5): [False, True, False, True], (0, 6): [False, True, False, True], (0, 7): [False, True, False, True], (0, 8): [False, True, False, True], (0, 9): [True, False, False, True], (0, 10): [False, False, True, True], (0, 11): [False, True, False, True], (0, 12): [False, True, False, True], (0, 13): [False, True, False, True], (0, 14): [False, True, False, True], (0, 15): [True, False, False, True], (1, 0): [False, False, True, True], (1, 1): [False, False, False, True], (1, 2): [False, True, False, False], (1, 3): [False, True, False, True], (1, 4): [False, True, False, False], (1, 5): [False, False, False, True], (1, 6): [False, True, False, True], (1, 7): [False, True, False, True], (1, 8): [True, False, False, True], (1, 9): [True, False, True, False], (1, 10): [True, False, True, False], (1, 11): [False, False, True, True], (1, 12): [True, False, False, True], (1, 13): [False, False, True, True], (1, 14): [True, False, False, True], (1, 15): [True, False, True, False], (2, 0): [True, False, True, False], (2, 1): [True, False, True, False], (2, 2): [False, False, True, True], (2, 3): [False, True, False, True], (2, 4): [False, True, False, True], (2, 5): [False, True, False, False], (2, 6): [False, True, False, True], (2, 7): [False, True, False, True], (2, 8): [True, True, False, False], (2, 9): [True, True, True, False], (2, 10): [True, False, True, False], (2, 11): [True, False, True, False], (2, 12): [False, True, True, False], (2, 13): [True, True, False, False], (2, 14): [False, True, True, False], (2, 15): [True, True, False, False], (3, 0): [True, False, True, False], (3, 1): [True, False, True, False], (3, 2): [False, True, True, False], (3, 3): [False, True, False, True], (3, 4): [False, True, False, True], (3, 5): [False, True, False, True], (3, 6): [False, True, False, True], (3, 7): [False, True, False, True], (3, 8): [False, True, False, True], (3, 9): [False, True, False, True], (3, 10): [True, True, False, False], (3, 11): [False, True, True, False], (3, 12): [False, True, False, True], (3, 13): [False, True, False, True], (3, 14): [False, True, False, True], (3, 15): [True, False, False, True], (4, 0): [True, False, True, False], (4, 1): [True, False, True, False], (4, 2): [False, False, True, True], (4, 3): [False, True, False, True], (4, 4): [False, True, False, True], (4, 5): [False, True, False, True], (4, 6): [False, True, False, True], (4, 7): [True, False, False, True], (4, 8): [False, False, True, True], (4, 9): [True, False, False, True], (4, 10): [False, True, True, True], (4, 11): [False, True, False, True], (4, 12): [False, True, False, True], (4, 13): [False, False, False, True], (4, 14): [True, False, False, True], (4, 15): [True, False, True, False], (5, 0): [True, False, True, False], (5, 1): [True, False, True, False], (5, 2): [False, True, True, False], (5, 3): [False, True, False, True], (5, 4): [False, True, False, True], (5, 5): [False, True, False, True], (5, 6): [True, False, False, True], (5, 7): [False, True, True, False], (5, 8): [True, False, False, False], (5, 9): [False, True, True, False], (5, 10): [False, True, False, True], (5, 11): [False, True, False, True], (5, 12): [True, False, False, True], (5, 13): [True, False, True, False], (5, 14): [False, True, True, False], (5, 15): [True, True, False, False], (6, 0): [True, False, True, False], (6, 1): [True, False, True, False], (6, 2): [False, True, True, True], (6, 3): [False, True, False, True], (6, 4): [False, True, False, True], (6, 5): [True, False, False, True], (6, 6): [False, True, True, False], (6, 7): [True, False, False, True], (6, 8): [True, True, True, False], (6, 9): [False, True, True, True], (6, 10): [False, True, False, True], (6, 11): [True, False, False, True], (6, 12): [True, False, True, False], (6, 13): [False, False, True, False], (6, 14): [False, False, False, True], (6, 15): [True, False, False, True], (7, 0): [False, False, True, False], (7, 1): [False, False, False, False], (7, 2): [False, False, False, True], (7, 3): [False, True, False, True], (7, 4): [True, False, False, True], (7, 5): [False, True, True, False], (7, 6): [True, False, False, True], (7, 7): [False, False, True, False], (7, 8): [True, False, False, True], (7, 9): [False, False, True, True], (7, 10): [True, False, False, True], (7, 11): [True, False, True, False], (7, 12): [True, False, True, False], (7, 13): [True, False, True, False], (7, 14): [True, False, True, False], (7, 15): [True, False, True, False], (8, 0): [True, False, True, False], (8, 1): [True, False, True, False], (8, 2): [True, False, True, False], (8, 3): [True, False, True, True], (8, 4): [False, False, True, False], (8, 5): [False, True, False, True], (8, 6): [True, False, False, False], (8, 7): [False, True, True, False], (8, 8): [True, True, False, False], (8, 9): [True, False, True, False], (8, 10): [True, True, True, False], (8, 11): [False, False, True, False], (8, 12): [True, True, False, False], (8, 13): [True, False, True, False], (8, 14): [True, False, True, False], (8, 15): [True, False, True, False], (9, 0): [True, False, True, False], (9, 1): [True, False, True, False], (9, 2): [True, False, True, False], (9, 3): [False, False, True, False], (9, 4): [True, True, False, False], (9, 5): [False, False, True, True], (9, 6): [True, True, False, False], (9, 7): [False, False, True, True], (9, 8): [True, True, False, True], (9, 9): [True, False, True, False], (9, 10): [False, False, True, True], (9, 11): [False, True, False, False], (9, 12): [True, False, False, True], (9, 13): [True, True, True, False], (9, 14): [True, False, True, False], (9, 15): [True, False, True, False], (10, 0): [True, False, True, False], (10, 1): [True, False, True, False], (10, 2): [False, False, True, False], (10, 3): [True, True, False, False], (10, 4): [False, False, True, True], (10, 5): [True, True, False, False], (10, 6): [False, False, True, True], (10, 7): [True, False, False, False], (10, 8): [False, False, True, True], (10, 9): [True, True, False, False], (10, 10): [False, True, True, False], (10, 11): [False, True, False, True], (10, 12): [True, False, False, False], (10, 13): [False, False, True, True], (10, 14): [True, False, False, False], (10, 15): [True, False, True, False], (11, 0): [True, False, True, False], (11, 1): [False, True, True, False], (11, 2): [True, True, False, False], (11, 3): [False, False, True, True], (11, 4): [True, True, False, False], (11, 5): [False, False, True, True], (11, 6): [True, True, False, False], (11, 7): [True, True, True, False], (11, 8): [True, False, True, False], (11, 9): [False, False, True, True], (11, 10): [True, False, False, True], (11, 11): [True, False, True, True], (11, 12): [False, True, True, False], (11, 13): [True, False, False, False], (11, 14): [True, False, True, False], (11, 15): [True, False, True, False], (12, 0): [True, False, True, False], (12, 1): [True, False, True, True], (12, 2): [False, False, True, True], (12, 3): [True, True, False, False], (12, 4): [False, False, True, True], (12, 5): [False, False, False, False], (12, 6): [False, True, False, True], (12, 7): [True, False, False, True], (12, 8): [True, False, True, False], (12, 9): [True, False, True, False], (12, 10): [True, False, True, False], (12, 11): [False, False, True, False], (12, 12): [True, False, False, True], (12, 13): [True, False, True, False], (12, 14): [True, False, True, False], (12, 15): [True, False, True, False], (13, 0): [True, False, True, False], (13, 1): [False, False, True, False], (13, 2): [True, True, False, False], (13, 3): [False, False, True, True], (13, 4): [True, True, False, False], (13, 5): [True, False, True, False], (13, 6): [False, True, True, True], (13, 7): [True, False, False, False], (13, 8): [False, True, True, False], (13, 9): [True, True, False, False], (13, 10): [True, False, True, False], (13, 11): [True, False, True, False], (13, 12): [True, False, True, False], (13, 13): [True, False, True, False], (13, 14): [True, False, True, False], (13, 15): [True, False, True, False], (14, 0): [True, False, True, False], (14, 1): [False, True, True, False], (14, 2): [False, True, False, True], (14, 3): [False, True, False, False], (14, 4): [False, True, False, True], (14, 5): [False, True, False, False], (14, 6): [False, True, False, True], (14, 7): [False, True, False, False], (14, 8): [False, True, False, True], (14, 9): [True, True, False, True], (14, 10): [False, True, True, False], (14, 11): [True, True, False, False], (14, 12): [False, True, True, False], (14, 13): [True, True, False, False], (14, 14): [True, False, True, False], (14, 15): [True, False, True, False], (15, 0): [False, True, True, False], (15, 1): [False, True, False, True], (15, 2): [False, True, False, True], (15, 3): [False, True, False, True], (15, 4): [False, True, False, True], (15, 5): [False, True, False, True], (15, 6): [False, True, False, True], (15, 7): [False, True, False, True], (15, 8): [False, True, False, True], (15, 9): [False, True, False, True], (15, 10): [False, True, False, True], (15, 11): [False, True, False, True], (15, 12): [False, True, False, True], (15, 13): [False, True, False, True], (15, 14): [False, True, False, False], (15, 15): [False, False, False, False]}
        self.q_table = np.zeros((self.mazeWidth, self.mazeHeight, 4))
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.goal_positions = self.get_goal_position()
        self.max_episodes = max_episodes
        self.unfeasable_path_reward = -10000
        self.unfeasable_paths = []

    def get_possible_actions_next_states(self, state=None):
        if state is None:
            state = self.curr_position
        actions_next_states = []
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = (nx, ny)
                if not self.wall_between(state, direction) and (direction, state) not in self.unfeasable_paths:
                    # if :
                    actions_next_states.append((direction, neighbor_value))
                else:
                    self.q_table[state[0]][state[1]][direction] = -100000
        return actions_next_states

    def is_dead_end(self, position):
        return sum(self.walls[position]) == 3
    
    def get_unfeasable_paths(self, position, visited = None, recur = False):
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
            action = (self.get_possible_actions_next_states(position)[0][0] +2) % 4
            # self.unfeasable_paths.append((action, position))
            API.setColor(position[0], position[1], 'b')

        actions_next_states = self.get_possible_actions_next_states(position)
        for act_state in actions_next_states:
            state = act_state[1]
            if state not in visited:
                walls_true = [wall == True for wall in self.walls[state]]
                # log(f'State = {state}, walls = {walls_true}')
                action = (act_state[0] + 2) % 4
                self.unfeasable_paths.append((action, state))
                API.setColor(state[0], state[1], 'b')
                if sum(walls_true) >= 2:  # Dead end or almost dead end

                    self.get_unfeasable_paths(state, visited, recur=True)

    def choose_action(self, state, debug = False):
        # log(self.epsilon)
        actions_next_states = self.get_possible_actions_next_states(state)
        if len(actions_next_states) == 1:
            if debug:
                log(f'debug: {actions_next_states}')
            return actions_next_states[0][0]
        if random.random() < self.epsilon:
            if debug:
                log(f'debug: {actions_next_states}')
            return random.choice(actions_next_states)[0]
        else:
            if debug:
                log(f'debug: {actions_next_states}')
            q_values = self.q_table[state[0], state[1], :]
            best_action = max(actions_next_states, key=lambda x: q_values[x[0]])[0]
            return best_action

    def get_reward(self, next_state):
        if next_state in self.goal_positions:
            return 100000
        elif self.is_dead_end(next_state):
            return self.unfeasable_path_reward
        else:
            min_distance = min(abs(next_state[0] - goal[0]) + abs(next_state[1] - goal[1]) for goal in self.goal_positions)
            log(-8 - min_distance)
            return -8 - min_distance

    def learn(self):
        state = self.curr_position
        action = self.choose_action(state)
        self.move_update_position(action)
        # dx, dy = self.directionVectors[action]
        # self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)
        next_state = self.curr_position
        reward = self.get_reward(next_state)
        next_action = self.choose_action(next_state)

        self.q_table[state[0], state[1], action] += self.alpha * (
            reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[state[0], state[1], action]
        )
        log(f'q_value: {self.q_table[state[0], state[1], action]}')
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_sarsa(self):
        # API.clearAllColor()
        for episode in range(self.max_episodes):
            if episode < 10:
                self.epsilon = 1.0
            log(f'Running episode: {episode}')
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                self.learn()
            self.go_back_to_start()
            log(self.q_table)
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

import time

def main():
    log("Running floodfill and SARSA algorithm...")
    exp = SARSAExplore(max_episodes=100)
    exp.move_and_floodfill()
    log(exp.walls)

    exp.go_back_to_start()
    API.clearAllColor()
    for state in exp.positions:
        API.setText(state[0], state[1], f'{state[0]}, {state[1]}')
    
    for state in exp.positions:
        try:
            exp.get_unfeasable_paths(state)
        except Exception as e:
            log(f'state: {state}, err: {e}')

    for path in exp.unfeasable_paths:
        log(path)
    time.sleep(3)
    exp.run_sarsa()
    # log(exp.q_table)

if __name__ == "__main__":
    main()
