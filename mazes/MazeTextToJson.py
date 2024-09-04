import glob
import json
import os
from matplotlib import pyplot as plt


def convert_to_dictionary(maze_str):
    maze_lines = maze_str.strip().split('\n')[::-1]
    maze_dict = {}

    for j in range(1, len(maze_lines), 2):
        for i in range(0, len(maze_lines[0]), 4):
            north = (maze_lines[j + 1][i:i + 4].__contains__('-')) if j + 1 < len(maze_lines) else True
            east = (maze_lines[j][i + 4].__contains__('|')) if i + 4 < len(maze_lines[0]) else True
            south = (maze_lines[j - 1][i:i + 4].__contains__('-')) if j - 1 >= 0 else True
            west = (maze_lines[j][i] == '|') if i != 0 else True

            x, y = i // 4, j // 2
            if x < 16 and y < 16:
                maze_dict[(x, y)] = [north, east, south, west]

    return maze_dict


def save_maze(maze_dict, filename):
    maze_dict_str_keys = {str(k): v for k, v in maze_dict.items()}
    with open(filename, 'w') as json_file:
        json.dump(maze_dict_str_keys, json_file, indent=4)


output_dir = 'competition_json'
os.makedirs(output_dir, exist_ok=True)

for filename in glob.glob(os.path.join('compitetion', '*.txt')):
    with open(filename) as file:
        maze_txt = file.read()
        maze_dict = convert_to_dictionary(maze_txt)
        json_filename = os.path.join('competition_json', os.path.splitext(os.path.basename(filename))[0] + '.json')
        save_maze(maze_dict, json_filename)


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
        if wall[0]:
            ax.plot([x, x + 1], [y + 1, y + 1], color=color)
        if wall[1]:
            ax.plot([x + 1, x + 1], [y, y + 1], color=color)
        if wall[2]:
            ax.plot([x, x + 1], [y, y], color=color)
        if wall[3]:
            ax.plot([x, x], [y, y + 1], color=color)
    plt.xlim(0, 16)
    plt.ylim(0, 16)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


draw_maze('competition_json/AAMC15Maze.json')
