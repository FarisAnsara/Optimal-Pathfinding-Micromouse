import numpy as np
import json
import os
import random
import matplotlib.pyplot as plt
from collections import deque


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = {(x, y): [True, True, True, True] for x in range(width) for y in range(height)}
        self.visited = {(x, y): False for x in range(width) for y in range(height)}
        self.start_position = (0, 0)
        self.goal_positions = [(width // 2, height // 2), (width // 2 - 1, height // 2),
                               (width // 2, height // 2 - 1), (width // 2 - 1, height // 2 - 1)]

    def generate_maze(self):
        self.visited[self.start_position] = True
        self.stack = [self.start_position]
        while self.stack:
            current_cell = self.stack[-1]
            x, y = current_cell
            neighbors = self.get_unvisited_neighbors(x, y)
            if neighbors:
                next_cell = random.choice(neighbors)
                nx, ny = next_cell
                self.remove_wall(current_cell, next_cell)
                self.visited[next_cell] = True
                self.stack.append(next_cell)
            else:
                self.stack.pop()

        if not self.is_solvable():
            self.__init__(self.width, self.height)
            self.generate_maze()
        else:
            self.create_multiple_paths()

        self.goal_positions_setup()
        if not self.is_solvable():
            return

    def get_unvisited_neighbors(self, x, y):
        neighbors = []
        if x > 0 and not self.visited[(x - 1, y)]:
            neighbors.append((x - 1, y))
        if x < self.width - 1 and not self.visited[(x + 1, y)]:
            neighbors.append((x + 1, y))
        if y > 0 and not self.visited[(x, y - 1)]:
            neighbors.append((x, y - 1))
        if y < self.height - 1 and not self.visited[(x, y + 1)]:
            neighbors.append((x, y + 1))
        return neighbors

    def remove_wall(self, current, next):
        cx, cy = current
        nx, ny = next
        if cx == nx:
            if cy > ny:
                self.walls[(cx, cy)][2] = False
                self.walls[(nx, ny)][0] = False
            else:
                self.walls[(cx, cy)][0] = False
                self.walls[(nx, ny)][2] = False
        elif cy == ny:
            if cx > nx:
                self.walls[(cx, cy)][3] = False
                self.walls[(nx, ny)][1] = False
            else:
                self.walls[(cx, cy)][1] = False
                self.walls[(nx, ny)][3] = False

    def goal_positions_setup(self):
        # Define goal positions
        goal_positions = [(8, 8), (7, 8), (8, 7), (7, 7)]
        directions = [[0, 1], [0, 3], [1, 2], [2, 3]]

        # Close off all walls within the goal area
        for i, val in enumerate(goal_positions):
            self.walls[val] = [False, False, False, False]
            for dir in directions[i]:
                self.walls[val][dir] = True

        # Randomly select one cell in the goal positions to be the entrance
        entrance_position = random.choice(goal_positions)
        i = goal_positions.index(entrance_position)
        entrance_direction = random.choice(directions[i])
        # entrance_directions = [0, 1, 2, 3]  # North, East, South, West
        # random.shuffle(entrance_directions)

        # for direction in entrance_directions:
        dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][entrance_direction]
        ex, ey = entrance_position[0] + dx, entrance_position[1] + dy
        if self.is_within_bounds(ex, ey):
            self.remove_wall(entrance_position, (ex, ey))

    def add_wall(self, current, next):
        cx, cy = current
        nx, ny = next
        if cx == nx:
            if cy > ny:
                self.walls[(cx, cy)][2] = True
                self.walls[(nx, ny)][0] = True
            else:
                self.walls[(cx, cy)][0] = True
                self.walls[(nx, ny)][2] = True
        elif cy == ny:
            if cx > nx:
                self.walls[(cx, cy)][3] = True
                self.walls[(nx, ny)][1] = True
            else:
                self.walls[(cx, cy)][1] = True
                self.walls[(nx, ny)][3] = True

    def create_multiple_paths(self):
        """Use BFS to find and remove walls to create multiple paths to the goal positions."""
        for goal in self.goal_positions:
            queue = deque([goal])
            visited = set([goal])
            parent_map = {}

            while queue:
                current = queue.popleft()
                x, y = current

                # Check if we've found a path to the start
                if current == self.start_position:
                    continue

                for direction, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
                    neighbor = (x + dx, y + dy)

                    # Check if neighbor is within bounds and not visited
                    if self.is_within_bounds(x + dx, y + dy) and neighbor not in visited:
                        if not self.walls[(x, y)][direction]:  # Check if there is no wall
                            queue.append(neighbor)
                            visited.add(neighbor)
                            parent_map[neighbor] = current

                        elif random.random() < 0.1:  # Randomly remove a wall
                            self.remove_wall((x, y), neighbor)
                            queue.append(neighbor)
                            visited.add(neighbor)
                            parent_map[neighbor] = current

            # Now we want to ensure we have at least 3 paths by removing additional walls if needed
            unique_paths = set()
            for position in visited:
                unique_paths.add(position)
                if len(unique_paths) >= 3:
                    break

            # if len(unique_paths) < 3:
            #     self.remove_random_walls_for_additional_paths(unique_paths)

    def remove_random_walls_for_additional_paths(self, unique_paths):
        """Remove random walls to create additional paths."""
        for position in unique_paths:
            x, y = position
            for direction, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
                neighbor = (x + dx, y + dy)
                if self.is_within_bounds(x + dx, y + dy):
                    if random.random() < 0.3:  # Randomly remove a wall
                        self.remove_wall((x, y), neighbor)

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_solvable(self):
        """Check if the maze is solvable by ensuring at least one path to the goal positions."""
        stack = [self.start_position]
        visited = {self.start_position}
        while stack:
            current = stack.pop()
            if current in self.goal_positions:
                return True
            x, y = current
            for direction, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
                if not self.walls[(x, y)][direction]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
        return False

    def save_maze(self, filename):
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.walls.items()}, f)

    def load_maze(self, filename):
        with open(filename, 'r') as f:
            self.walls = {eval(k): v for k, v in json.load(f).items()}


def get_goal_position():
    center_x, center_y = 16 // 2, 16 // 2
    return [(center_x, center_y), (center_x - 1, center_y), (center_x, center_y - 1), (center_x - 1, center_y - 1)]


def draw_maze(maze_file):
    with open(maze_file, 'r') as f:
        walls = {eval(k): v for k, v in json.load(f).items()}

    fig, ax = plt.subplots()
    goal_positions = get_goal_position()
    for (x, y), wall in walls.items():
        color = 'r' if (x, y) in goal_positions else 'k'
        if wall[0]:  # NORTH
            ax.plot([x, x + 1], [y + 1, y + 1], color=color)
        if wall[1]:  # EAST
            ax.plot([x + 1, x + 1], [y, y + 1], color=color)
        if wall[2]:  # SOUTH
            ax.plot([x, x + 1], [y, y], color=color)
        if wall[3]:  # WEST
            ax.plot([x, x], [y, y + 1], color=color)
    plt.xlim(0, 16)
    plt.ylim(0, 16)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def generate_mazes(num_mazes, width, height, output_dir):
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i in range(num_mazes):
        maze_gen = MazeGenerator(width, height)
        maze_gen.generate_maze()
        maze_gen.save_maze(os.path.join(output_dir, f'maze_{i}.json'))

if __name__ == "__main__":
    generate_mazes(3000, 16, 16, "mazes")
    # draw_maze("Reinforcement_Learning\Deep_RL\mazes\maze_0.json")
    
