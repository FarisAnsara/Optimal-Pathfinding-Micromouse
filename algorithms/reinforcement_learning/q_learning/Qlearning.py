import numpy as np
from matplotlib import pyplot as plt

from algorithms.reinforcement_learning.RLSetup import RLSetup


class QLearning(RLSetup):
    def __init__(self, walls, epsilon=0.99, alpha=0.1, gamma=0.8, epsilon_decay=0.99, max_episodes=1000, min_epsilon=0.01,
                 maze_width=16, maze_height=16):
        super().__init__(walls=walls)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.max_episodes = max_episodes
        self.goal_positions = self.get_goal_position()
        self.episode = 0

    def learn(self):
        state = self.curr_position
        action = self.choose_action(state)
        old_orientation = self.orientation
        self.move_update_position(action)
        next_state = self.curr_position
        reward = self.get_reward(next_state, action, old_orientation, state)
        self.accumalated_reward += reward

        max_next_q_value = np.max(self.q_table[next_state[0], next_state[1], :])
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * max_next_q_value - self.q_table[state[0], state[1], action]
        )

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_qlearning(self):
        # Todo: implement Early stopping
        rewards = []
        for episode in range(self.max_episodes):
            self.accumalated_reward = 0
            self.episode = episode
            print(f'Running episode: {episode}')
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                self.learn()

            print(f'Prev: {self.previous_reward}, Current reward: {self.accumalated_reward}')
            print(f'stats: {self.get_stats()}')
            rewards.append(self.accumalated_reward)
            if self.early_stopping():
                print(f'stopped at episode: {episode}')
                break
            self.reset_env()
            self.previous_reward = self.accumalated_reward

        plt.figure()
        plt.plot(range(len(rewards)), rewards)
        plt.xlabel('Episodes')
        plt.ylabel('Accumulated Reward')
        plt.title('Qlearning Learning')
        plt.show()
