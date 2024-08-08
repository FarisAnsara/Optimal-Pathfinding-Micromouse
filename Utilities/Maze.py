import json

from matplotlib import pyplot as plt


class Maze:

    @staticmethod
    def load_maze(filename):
        with open(filename, 'r') as f:
            walls = {tuple(k): v for k, v in json.load(f).items()}

        return walls

    @staticmethod
    def draw_maze(maze_file):
        with open(maze_file, 'r') as f:
            walls = {eval(k): v for k, v in json.load(f).items()}

        fig, ax = plt.subplots()
        for (x, y), wall in walls.items():
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