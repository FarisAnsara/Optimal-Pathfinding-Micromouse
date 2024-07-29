import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Adding parent directories to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utilities import API
from Reinforcement_Learning import RLMazeOffline


class DynaQLearningOffline(RLMazeOffline):
    def __init__(self, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.99, max_episodes=50, min_epsilon=0.01,
                 maze_width=16, maze_height=16, reward_threshold=1, planning_steps=100):
        super().__init__()
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.max_episodes = max_episodes
        self.goal_positions = self.get_goal_position()
        self.visited_states = np.zeros((maze_width, maze_height))
        self.reward_threshold = reward_threshold
        self.accumulated_reward = 0
        self.planning_steps = planning_steps
        self.episode = 0
        self.model = []

    def learn(self):
        self.update_walls(position=self.curr_position, orientation=self.orientation)
        state = self.curr_position
        API.setColor(state[0], state[1], 'b')
        action = self.choose_action(state)
        self.move_update_position(action, offline=True)
        # dx, dy = self.directionVectors[action]
        # self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)
        next_state = self.curr_position
        log(f'state: {state}, next_state = {next_state}, action: {action}')

        self.update_walls(position=self.curr_position, orientation=self.orientation)
        reward = self.get_reward(next_state)
        self.accumulated_reward += reward
        max_next_q_value = np.max(self.q_table[next_state[0], next_state[1], :])
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * max_next_q_value - self.q_table[state[0], state[1], action]
        )

        self.model.append((state, action, reward, next_state))

        if self.episode > 0:
            for _ in range(self.planning_steps):
                s, a, r, ns = random.choice(self.model)
                max_next_q_value = np.max(self.q_table[ns[0], ns[1], :])
                self.q_table[s[0], s[1], a] += self.alpha * (
                        r + self.gamma * max_next_q_value - self.q_table[s[0], s[1], a]
                )
        self.visited_states[next_state[0], next_state[1]] += 1
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        self.update_q_vals_on_API()

    def run_DynaQLearning(self):
        # Todo: implement Early stopping
        rewards = []
        prev_reward = 0
        for episode in range(self.max_episodes):
            self.accumulated_reward = 0
            # if episode < 5:
            #     self.epsilon = 0.99
            self.episode = episode
            log(f'Running episode: {episode}')
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                self.learn()

            log(f'Prev: {prev_reward}, Current reward: {self.accumulated_reward}')
            log(np.abs(self.accumulated_reward - prev_reward))
            rewards.append(self.accumulated_reward)
            prev_reward = self.accumulated_reward
            API.ackReset()
            self.curr_position = self.start_position
            self.orientation = self.NORTH

            # Displaying the max Q-values
            self.update_q_vals_on_API()

        plt.figure()
        plt.plot(range(len(rewards)), rewards)
        plt.xlabel('Episodes')
        plt.ylabel('Accumulated Reward')
        plt.title('Q-learning Online Learning')
        plt.show()

    def update_q_vals_on_API(self):
        for i in range(self.q_table.shape[0]):
            for j in range(self.q_table.shape[1]):
                max_val = np.max(self.q_table[i, j])
                API.setText(i, j, str(round(max_val, 2)))  # Display the Q-value


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


from Classical_Algorithms import FloodFill


def main():
    log("Running DynaQlearning algorithm offline...")
    exp = DynaQLearningOffline()
    # flood = FloodFill()
    exp.move_and_floodfill()
    # exp.get_all_unfeasable()
    exp.run_DynaQLearning()


if __name__ == "__main__":
    main()
