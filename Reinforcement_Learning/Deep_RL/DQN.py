import numpy as np
import random
import sys
from Flood import Explore

class DQNExplore(Explore):
    def __init__(self, model, epsilon=0.9, alpha=0.1, gamma=0.9, epsilon_decay=0.99, min_epsilon=0.01, max_episodes=100):
        super().__init__()
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.max_episodes = max_episodes
        self.replay_buffer = []
        self.buffer_size = 10000
        self.batch_size = 64
        self.goal_positions = self.get_goal_position()

    def get_possible_actions_next_states(self, state=None):
        if state is None:
            state = self.curr_position
        actions_next_states = []
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = (nx, ny)
                if not self.wall_between(state, direction):
                    actions_next_states.append((direction, neighbor_value))
        return actions_next_states

    def policy(self, state=None):
        if state is None:
            state = self.curr_position
        if random.random() < self.epsilon:
            return random.choice(self.get_possible_actions_next_states(state))
        else:
            q_values = self.model.predict(np.array(state).reshape(1, -1))
            actions_next_states = self.get_possible_actions_next_states(state)
            best_action = max(actions_next_states, key=lambda x: q_values[0][x[0]])
            return best_action

    def get_reward(self, next_state):
        if next_state in self.goal_positions:
            return 1000
        elif self.is_dead_end(self.curr_position):
            return -1000
        else:
            return -1

    def is_dead_end(self, position):
        x, y = position
        wall_count = sum(self.walls[position])
        return wall_count == 3

    def store_experience(self, state, action, reward, next_state):
        if len(self.replay_buffer) > self.buffer_size:
            self.replay_buffer.pop(0)
        self.replay_buffer.append((state, action, reward, next_state))

    def learn_from_experience(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        batch = random.sample(self.replay_buffer, self.batch_size)
        for state, action, reward, next_state in batch:
            q_update = reward
            if next_state not in self.goal_positions:
                q_update = reward + self.gamma * np.max(self.model.predict(np.array(next_state).reshape(1, -1)))
            q_values = self.model.predict(np.array(state).reshape(1, -1))
            q_values[0][action] = q_update
            self.model.fit(np.array(state).reshape(1, -1), q_values, verbose=0)

    def run_dqn(self):
        for episode in range(self.max_episodes):
            self.curr_position = self.start_position
            while self.curr_position not in self.goal_positions:
                state = self.curr_position
                action, next_state = self.policy(state)
                reward = self.get_reward(next_state)
                self.store_experience(state, action, reward, next_state)
                self.learn_from_experience()
                self.move_update_position(action)
                self.curr_position = next_state
                self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            self.go_back_to_start()

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense

    # Define the DQN model
    model = Sequential([
        Dense(24, input_dim=2, activation='relu'),
        Dense(24, activation='relu'),
        Dense(4, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')

    log("Running floodfill and DQN algorithm...")
    exp = DQNExplore(model=model, max_episodes=1000)
    exp.move_and_floodfill()  # Initial exploration with flood fill
    exp.go_back_to_start()
    exp.run_dqn()
    log("DQN training completed.")

if __name__ == "__main__":
    main()
