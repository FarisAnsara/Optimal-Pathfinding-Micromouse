import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../../algorithms/reinforcement_learning/dynaq', '..', '..', '..')))

from MMS.mms_integration.reinforcement_learning import RLOffline


class DynaQSarsaOffline(RLOffline):
    def __init__(self, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.99, max_episodes=50, min_epsilon=0,
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
        action = self.choose_action(state)
        old_orientation = self.orientation
        self.move_update_position(action, offline=True)
        next_state = self.curr_position
        self.update_walls(position=self.curr_position, orientation=self.orientation)
        reward = self.get_reward(next_state, old_orientation)
        self.accumulated_reward += reward
        next_action = self.choose_action(next_state)
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[
            state[0], state[1], action]
        )

        self.model.append((state, action, reward, next_state))

        if self.episode > 0:
            for _ in range(self.planning_steps):
                s, a, r, ns = random.choice(self.model)
                na = self.choose_action(ns)
                n_q_value = self.q_table[ns[0], ns[1], na]
                self.q_table[s[0], s[1], a] += self.alpha * (
                        r + self.gamma * n_q_value - self.q_table[s[0], s[1], a]
                )

        self.visited_states[next_state[0], next_state[1]] += 1
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_DynaQ_sarsa(self):
        rewards = []
        prev_reward = 0
        for episode in range(self.max_episodes):
            self.accumulated_reward = 0
            self.episode = episode
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                self.learn()

            rewards.append(self.accumulated_reward)
            prev_reward = self.accumulated_reward
            self.reset_env()
            self.curr_position = self.start_position
            self.orientation = self.NORTH

            self.update_q_vals_on_API()

        plt.figure()
        plt.plot(range(len(rewards)), rewards)
        plt.xlabel('Episodes')
        plt.ylabel('Accumulated Reward')
        plt.title('DynaQ-Sarsa Offline Learning')
        plt.show()


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running DynaQSarsa algorithm offline...")
    exp = DynaQSarsaOffline()
    exp.move_and_floodfill()
    exp.reset_env()
    exp.run_DynaQ_sarsa()


if __name__ == "__main__":
    main()
