import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from algorithms.mms_integration import API
from algorithms.mms_integration.reinforcement_learning import RLMazeOffline


class SarsaOffline(RLMazeOffline):
    def __init__(self, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.99, max_episodes=200, min_epsilon=0.01,
                 maze_width=16, maze_height=16):
        super().__init__()
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.max_episodes = max_episodes
        self.goal_positions = self.get_goal_position()
        self.accumulated_reward = 0
        self.episode = 0

    def learn(self):
        self.update_walls(position=self.curr_position, orientation=self.orientation)
        state = self.curr_position
        action = self.choose_action(state)
        self.move_update_position(action, offline=True)
        next_state = self.curr_position
        self.update_walls(position=self.curr_position, orientation=self.orientation)
        reward = self.get_reward(next_state)
        self.accumulated_reward += reward
        next_action = self.choose_action(next_state)
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[
            state[0], state[1], action]
        )

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_sarsa(self):
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
        plt.title('Sarsa Offline Learning')
        plt.show()


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running DynaQSarsa algorithm offline...")
    exp = SarsaOffline()
    exp.move_and_floodfill()
    exp.run_sarsa()


if __name__ == "__main__":
    main()
