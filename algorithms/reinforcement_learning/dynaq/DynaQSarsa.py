import random
import numpy as np
from matplotlib import pyplot as plt

from algorithms.reinforcement_learning.RL import RL


class DynaQSarsa(RL):
    def __init__(self, walls, epsilon=0.99, alpha=0.1, gamma=0.9, epsilon_decay=0.99, max_episodes=100, min_epsilon=0.01,
                 maze_width=16, maze_height=16, planning_steps=125,arbitrary=False):
        super().__init__(walls=walls)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.max_episodes = max_episodes
        self.goal_positions = self.get_goal_position()
        self.planning_steps = planning_steps
        # self.model = []
        self.model = {}
        self.arbitrary = arbitrary

    def learn(self):
        state = self.curr_position
        action = self.choose_action(state)
        old_orientation = self.orientation
        self.move_update_position(action)
        next_state = self.curr_position
        reward = self.get_reward(next_state, action, old_orientation, state, dynaq=True, arbitrary=self.arbitrary)
        self.accumalated_reward += reward

        next_action = self.choose_action(next_state)
        self.q_table[state[0], state[1], action] += self.alpha * (
                reward + self.gamma * self.q_table[next_state[0], next_state[1], next_action] - self.q_table[
            state[0], state[1], action]
        )

        # self.model.append((state, action, reward, next_state))
        self.model[(state, action)] = (reward, next_state)

        # if self.episode > 0:
        #     for _ in range(self.planning_steps):
        #         # s, a, r, ns = random.choice(self.model)
        #         s, a = random.choice(list(self.model.keys()))
        #         r, ns = self.model[(s, a)]
        #         na = self.choose_action(ns)
        #         n_q_value = self.q_table[ns[0], ns[1], na]
        #         self.q_table[s[0], s[1], a] += self.alpha * (
        #                 r + self.gamma * n_q_value - self.q_table[s[0], s[1], a]
        #     )

        if self.episode > 0:
            for _ in range(self.planning_steps):
                # s, a, r, ns = random.choice(self.model)
                s, a = random.choice(list(self.model.keys()))
                r, ns = self.model[(s, a)]
                max_next_q_value = np.max(self.q_table[ns[0], ns[1], :])
                self.q_table[s[0], s[1], a] += self.alpha * (
                        r + self.gamma * max_next_q_value - self.q_table[s[0], s[1], a]
                )

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_dyna_sarsa(self):
        paths_time_rewards = {}
        agents_succeeded = 0
        agent = 0
        agents_failed = 0
        while agents_succeeded < 3:
            agent += 1
            print(f'running agent {agent}')
            self.get_all_unfeasible()
            rewards = []
            episode_zero_steps = 0
            for episode in range(self.max_episodes):
                steps = 0
                # print(f'runnign episode: {episode}')
                self.accumalated_reward = 0
                self.episode = episode
                self.curr_position = self.start_position
                self.path.append(self.start_position)
                while self.curr_position not in self.goal_positions:
                    self.learn()
                    steps += 1
                    # print(self.curr_position, steps)
                    if steps > episode_zero_steps + 5000 and episode != 0:
                        # agents_failed += 1
                        print(f'agent: {agent} failed')
                        # self.fails = True
                        break

                # print(f'episode: {episode}, steps: {steps}')
                rewards.append(self.accumalated_reward)
                if self.early_stopping():
                    break
                self.reset_env()
                self.previous_reward = self.accumalated_reward
                # if agents_failed >= 3:
                #     print(f'agent: {agent} failed, moving on to use distance')
                #     self.fails = True
                #     agents_failed = 0
                #     break
                if steps > episode_zero_steps + 5000 and episode != 0:
                    break
                if episode == 0:
                    episode_zero_steps = steps if steps <= 5000 else 5000

            if self.path:
                paths_time_rewards[agent] = (self.path, self.get_time_from_path(), rewards, self.q_table)
                agents_succeeded += 1
            else:
                agents_failed += 1
            self.__init__(walls=self.walls, arbitrary=self.arbitrary)

        min_time_agent = min(paths_time_rewards, key=lambda k: paths_time_rewards[k][1])
        min_time_path, min_time, corresponding_rewards, min_time_q_table = paths_time_rewards[min_time_agent]
        self.path = min_time_path
        self.q_table = min_time_q_table

        end_memory = self.memory_usage()
        self.total_memory_used = end_memory - self.start_memory
        # print(f'Choose path: {self.path}, time: {min_time}')


        # plt.figure()
        # plt.plot(range(len(corresponding_rewards)), corresponding_rewards)
        # plt.xlabel('Episodes')
        # plt.ylabel('Accumulated Reward')
        # plt.title('DynaQSarsa Learning')
        # plt.show()
