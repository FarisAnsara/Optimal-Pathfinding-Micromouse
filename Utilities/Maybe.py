import API
from mazes.MazeGenerator import MazeGenerator
import os

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

maze_gen = MazeGenerator(width=16, height=16)

maze_0 = maze_gen.load_maze(filename=os.path.join(output_dir, 'mazes/maze_0.json'))

positions = maze_0.keys()

for pos in positions:
    values = maze_0[pos]
    i = 0
    for val in values:
        if val:
            API.setWall(pos[0], pos[1], i)
        i += 1

print(maze_0)


