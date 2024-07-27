import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Utilities import API, MoveMouse, Walls
from Classical_Algorithms import FloodFill
import numpy as np
import random
import sys
import time

class SARSAExplore(FloodFill):
    def __init__(self, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.999, max_episodes=100, min_epsilon=0.01, planning_steps=20, planning_steps_inc=0.9):
        super().__init__()
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
        self.model = []  # Model to store (state, action, reward, next_state)
        self.planning_steps = planning_steps
        self.planning_steps_inc = planning_steps_inc
        self.max_planning_steps = 100
        self.episode = 0
        self.visited_states = np.zeros((self.mazeWidth, self.mazeHeight))

    def get_possible_actions_next_states(self, state=None, unfeas = False):
        if state is None:
            state = self.curr_position
        actions_next_states = []
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = (nx, ny)
                if not self.wall_between(state, direction) and (direction, state) not in self.unfeasable_paths:
                    if unfeas or (direction + 2)%4 != self.orientation:
                        actions_next_states.append((direction, neighbor_value))
                else:
                    self.q_table[state[0]][state[1]][direction] = -100000
        return actions_next_states

    def is_dead_end(self, position):
        return sum(self.walls[position]) == 3

    def get_unfeasable_paths(self, position, visited=None, recur=False):
        if not self.is_dead_end(position):
            if not recur:
                return
        
        if visited is None:
            visited = set()

        visited.add(position)
        if self.is_dead_end(position):
            log(f'possible: {self.get_possible_actions_next_states(position)}')
            action = (self.get_possible_actions_next_states(position, unfeas=True)[0][0] + 2) % 4
            API.setColor(position[0], position[1], 'b')

        actions_next_states = self.get_possible_actions_next_states(position, unfeas=True)
        for act_state in actions_next_states:
            state = act_state[1]
            if state not in visited:
                walls_true = [wall == True for wall in self.walls[state]]
                action = (act_state[0] + 2) % 4
                self.unfeasable_paths.append((action, state))
                API.setColor(state[0], state[1], 'b')
                if sum(walls_true) >= 2:  # Dead end or almost dead end
                    self.get_unfeasable_paths(state, visited, recur=True)

    def choose_action(self, state, debug=False):
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
            reward = -8 
            log(reward)
            return reward

    def learn(self):
        state = self.curr_position
        action = self.choose_action(state)
        self.move_update_position(action)
        next_state = self.curr_position
        reward = self.get_reward(next_state)
        next_action = self.choose_action(next_state)

        self.q_table[state[0], state[1], action] += self.alpha * (
            reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[state[0], state[1], action]
        )
        log(f'q_value: {self.q_table[state[0], state[1], action]}, epsilon: {self.epsilon}')

        # Store the experience in the model
        self.model.append((state, action, reward, next_state))

        # Increment visit count
        self.visited_states[next_state[0], next_state[1]] += 1

        # Perform planning steps using Q-learning
        if self.episode > 0:
            for _ in range(self.planning_steps):
                s, a, r, ns = random.choice(self.model)
                max_next_q_value = np.max(self.q_table[ns[0], ns[1], :])
                self.q_table[s[0], s[1], a] += self.alpha * (
                    r + self.gamma * max_next_q_value - self.q_table[s[0], s[1], a]
                )
            self.planning_steps = min(self.max_planning_steps, int(self.planning_steps / self.planning_steps_inc))

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_sarsa(self):
        for episode in range(self.max_episodes):
            self.episode = episode
            if episode < 5:
                self.epsilon = 1.0
            log(f'Running episode: {self.episode}')
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                self.learn()
            self.go_back_to_start()
            self.turn_around()
            log(self.q_table)
            # self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    log("Running floodfill and SARSA algorithm...")
    exp = SARSAExplore(max_episodes=100)
    exp.move_and_floodfill()
    log(exp.walls)

    exp.go_back_to_start()
    exp.turn_around()
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

if __name__ == "__main__":
    main()
