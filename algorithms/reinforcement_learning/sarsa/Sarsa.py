import numpy as np
from matplotlib import pyplot as plt

from algorithms.reinforcement_learning.RLSetup import RLSetup


class Sarsa(RLSetup):
    def __init__(self, walls, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.99, max_episodes=1000, min_epsilon=0.01,
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
        next_action = self.choose_action(next_state)
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[
            state[0], state[1], action]
        )

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_sarsa(self):
        paths_time_rewards = {}
        for agent in range(self.num_agents):
            print(f'Running agent: {agent}')
            rewards = []
            for episode in range(self.max_episodes):
                self.accumalated_reward = 0
                self.episode = episode
                self.curr_position = self.start_position
                self.path.append(self.start_position)
                while self.curr_position not in self.goal_positions:
                    self.learn()

                rewards.append(self.accumalated_reward)
                if self.early_stopping():
                    print(f'stopped at episode: {episode}')
                    break
                self.reset_env()
                self.previous_reward = self.accumalated_reward

            if self.path:
                paths_time_rewards[agent] = (self.path, self.get_time_from_path(), rewards)
            if agent < self.num_agents - 1:
                self.__init__(walls=self.walls)

        min_time_agent = min(paths_time_rewards, key=lambda k: paths_time_rewards[k][1])
        min_time_path, min_time, corresponding_rewards = paths_time_rewards[min_time_agent]
        self.path = min_time_path
        print(f'Choose path: {self.path}, time: {min_time}')

        plt.figure()
        plt.xlabel('Episodes')
        plt.plot(range(len(corresponding_rewards)), corresponding_rewards)
        plt.ylabel('Accumulated Reward')
        plt.title('Sarsa Offline Learning')
        plt.show()
