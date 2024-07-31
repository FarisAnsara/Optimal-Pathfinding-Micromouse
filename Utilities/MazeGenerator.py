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
        self.goal_positions = [(width // 2, height // 2), (width // 2 - 1, height // 2), (width // 2, height // 2 - 1),
                               (width // 2 - 1, height // 2 - 1)]
        self.stack = []

    def generate_maze(self):
        self.stack.append(self.start_position)
        self.visited[self.start_position] = True
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

        # Ensure goal positions have only one opening
        self.ensure_goal_opening()

        if not self.is_solvable():
            self.walls = {(x, y): [True, True, True, True] for x in range(self.width) for y in range(self.height)}
            self.visited = {(x, y): False for x in range(self.width) for y in range(self.height)}
            self.stack = []
            self.generate_maze()

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
        goal_positions = [(8, 8), (7, 8), (8, 7), (7, 7)]
        for i, position in enumerate(goal_positions):
            self.walls[position] = [False for i in range(4)]
            self.walls[position][i] = True



    def ensure_goal_opening(self):
        # Ensure the goal positions have only one opening
        center_x, center_y = self.width // 2, self.height // 2
        goal_neighbors = [
            (center_x - 2, center_y - 1), (center_x - 2, center_y), (center_x - 1, center_y + 1),
            (center_x, center_y + 1),
            (center_x + 1, center_y), (center_x + 1, center_y - 1), (center_x, center_y - 2),
            (center_x - 1, center_y - 2)
        ]
        random.shuffle(goal_neighbors)
        opening_cell = goal_neighbors.pop()
        while not self.is_within_bounds(opening_cell[0], opening_cell[1]):
            opening_cell = goal_neighbors.pop()

        # Create an opening from the chosen cell to one of the goal cells
        self.remove_wall(opening_cell, (center_x - 1, center_y - 1))

        # Close other possible openings to the goal cells
        for neighbor in goal_neighbors:
            if self.is_within_bounds(neighbor[0], neighbor[1]):
                self.visited[neighbor] = True

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_solvable(self):
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
    center_x, center_y = 16 // 2, 16 // 2
    goal_positions = get_goal_position()
    print(goal_positions)
    for (x, y), wall in walls.items():
        if (x, y) in goal_positions:
            color = 'r'
        else:
            color = 'k'
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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    maze_gen = MazeGenerator(width, height)
    for i in range(num_mazes):
        maze_gen.generate_maze()
        maze_gen.save_maze(os.path.join(output_dir, f'maze_{i}.json'))


if __name__ == "__main__":
    # generate_mazes(1000, 16, 16, "mazes")
    draw_maze("mazes/maze_0.json")
    amz = MazeGenerator(16, 16)
    amz.goal_positions_setup()
