import numpy as np
import random
import sys
from Flood import Explore

class QLearningExplore(Explore):
    def __init__(self, epsilon = 0.99, alpha = 0.1, gamma = 0.999, epsilon_decay = 0.999, max_episodes=100, online_episodes=3, min_epsilon = 0.01):
        super().__init__()
        self.q_table = np.zeros((self.mazeWidth, self.mazeHeight, 4))
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.num_planning_steps = 10
        self.goal_positions = self.get_goal_position()  # Assuming first goal position for simplicity
        self.max_episodes = max_episodes
        self.online_episodes = online_episodes
        self.curr_position = self.start_position
        self.unfeasable_paths = []
        self.unfeasable_path_reward = -10000

    def get_possible_actions_next_states(self, state):
        if not state:
            state = self.curr_position
        actions_next_states = []
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = nx, ny
                if not self.wall_between(state, direction):
                    actions_next_states.append((direction, neighbor_value))
                else:
                    self.q_table[state[0], state[1], direction] = self.unfeasable_path_reward
        return actions_next_states

        return actions_next_states
    
    def is_dead_end(self, position):
        x, y = position
        wall_count = sum(self.walls[position])
        return wall_count == 3

    def policy(self, state = None):
        if not state:
            state = self.curr_position
        actions_next_states = self.get_possible_actions_next_states(state)
        if len(actions_next_states) == 1:
            return actions_next_states[0]
        if random.random() < self.epsilon:
            for val in actions_next_states:
                if val not in self.visited_state:
                    return val
            return random.choice(actions_next_states)
        else:
            q_values = self.q_table[self.curr_position[0], self.curr_position[1], :]
            best_action = max(actions_next_states, key=lambda x: q_values[x[0]])
            log(f'Best Action: {best_action}')
            return best_action

    def get_reward(self, next_state):
        if next_state in self.goal_positions:
            return 10000
        elif self.is_dead_end(self.curr_position):
            return self.unfeasable_path_reward
        else:
            return -1

    def learn(self):
        action, next_state = self.policy()
        if (action, next_state) not in self.visited_state:
            self.visited_state.add((action, next_state))
        reward = self.get_reward(next_state)
        log(f'rewward: {self.q_table[self.curr_position][action]}')
        next_max = np.max(self.q_table[next_state])
        self.q_table[self.curr_position][action] += self.alpha * (reward + self.gamma * next_max - self.q_table[self.curr_position][action])
        # self.curr_position = next_state
        self.move_update_position(action)
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_q_learning_online(self):
        for episode in range(self.max_episodes):
            if episode < 10:
                self.epsilon = 0.99
            log(f'running eopside:{episode}')
            log(self.q_table)
            self.curr_position = self.start_position
            self.visited_state = set()
            while self.curr_position not in self.goal_positions:
                log(self.epsilon)
                self.learn()
            self.go_back_to_start()

    def run_dyna_q_offline(self):
        pass

    def run_dyna_q_online(self):
        pass

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    log("Running floodfill and Q-learning algorithm...")
    exp = QLearningExplore(max_episodes=1000, online_episodes=3)
    exp.move_and_floodfill()  # Initial exploration with flood fill
    log(exp.walls)

    exp.go_back_to_start()
    exp.run_q_learning_online()
    log(exp.q_table)
    # exp.run_dyna_q_offline()  # Apply Dyna-Q for path optimization offline
    # log(exp.q_table)
    # exp.run_dyna_q_online()  # Apply Dyna-Q for path optimization online for 3 episodes
    # exp.take_shortest_path()

if __name__ == "__main__":
    main()
