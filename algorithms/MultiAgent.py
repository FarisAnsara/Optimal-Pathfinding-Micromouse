from algorithms.classical.floodfill.FloodFillTime import FloodFillTime
from algorithms.classical.bfs.BFSTime import BFSTime
from algorithms.reinforcement_learning.dynaq.DynaQLearning import DynaQLearning
from algorithms.utilities.Stats import Stats


class MultiAgent:

    def __init__(self, walls, maze_height=16, maze_width=16):
        flood = FloodFillTime(walls=walls, maze_height=maze_height, maze_width=maze_width)
        bfs = BFSTime(walls=walls, maze_width=maze_width, maze_height=maze_height)
        dyna = DynaQLearning(walls=walls)
        flood_path = flood.get_path_from_flood_map()
        bfs_path = bfs.find_shortest_path_to_goal()
        dyna.run_dyna_qlearning()
        dyna_path = dyna.get_path()
        self.paths = [flood_path, bfs_path, dyna_path]
        self.path = None

    def get_path(self):
        stats = Stats()
        time = stats.get_time_from_path(self.paths[0])
        chosen = self.paths[0]
        if len(self.paths) == 1:
            return chosen
        for path in self.paths[1:]:
            temp = stats.get_time_from_path(path)
            if temp < time:
                time = temp
                chosen = path

        return chosen
