import json
import os

import psutil
from matplotlib import pyplot as plt


class Utils:

    @staticmethod
    def get_goal_position(maze_width=16, maze_height=16):
        center_x, center_y = maze_width // 2, maze_height // 2
        return [(center_x, center_y), (center_x - 1, center_y), (center_x, center_y - 1), (center_x - 1, center_y - 1)]

    def is_goal_position(self, position):
        return position in self.get_goal_position()

    @staticmethod
    def load_maze(filename):
        with open(filename, 'r') as f:
            walls = {eval(k): v for k, v in json.load(f).items()}
        return walls

    @staticmethod
    def draw_maze(walls, path=None, goal_positions=None, dist_map = None, unfeasable=None):
        maze_width = 16
        maze_height = 16
        fig, ax = plt.subplots()
        for (x, y), wall in walls.items():
            color = 'white'
            if path and (x, y) in path:
                color = 'blue'
            elif goal_positions and (x, y) in goal_positions:
                color = 'red'
            if unfeasable:
                for val in unfeasable:
                    if (x, y) == val[1]:
                        color = '#575757'
                        if val[0] == 0:
                            text = '^'
                            position = (x+ 0.5, y + 0.75)
                        elif val[0] == 1:
                            text = '>'
                            position = (x+ 0.75, y + 0.5)
                        elif val[0] == 2:
                            text = 'v'
                            position = (x + 0.5, y + 0.25)
                        elif val[0] == 3:
                            position = (x + 0.25, y + 0.5)
                            text = '<'
                        else:
                            text = ''
                            position = (x+0.5, y+0.5)
                            ax.plot([x, x + 1], [y, y + 1], color='black')
                            ax.plot([x + 1, x], [y, y + 1], color='black')
                        font_size = min(7, 120 // max(maze_width, maze_height))  # Further reduced font size
                        ax.text(position[0], position[1], text, ha='center', va='center', fontsize=font_size)

            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color, alpha=0.3))
            if dist_map:
                font_size = min(7, 120 // max(maze_width, maze_height))  # Further reduced font size
                ax.text(x + 0.5, y + 0.5, f"{dist_map[x][y]:0.1f}", ha='center', va='center', fontsize=font_size)

            if wall[0]:  # NORTH
                ax.plot([x, x + 1], [y + 1, y + 1], color='black')
            if wall[1]:  # EAST
                ax.plot([x + 1, x + 1], [y, y + 1], color='black')
            if wall[2]:  # SOUTH
                ax.plot([x, x + 1], [y, y], color='black')
            if wall[3]:  # WEST
                ax.plot([x, x], [y, y + 1], color='black')

        plt.xlim(0, 16)
        plt.ylim(0, 16)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca()
        plt.show()

    @staticmethod
    def memory_usage():
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss / (1024 ** 2)  # in MB