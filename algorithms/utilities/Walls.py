class Walls:

    def __init__(self, maze_width, maze_height, walls):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.positions = [(n, m) for n in range(self.maze_width) for m in range(self.maze_height)]
        self.walls = walls
        self.visited_cells = {a: False for a in self.positions}
        self.start_position = (0, 0)
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1),
            self.EAST: (1, 0),
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }

    def wall_between(self, position, direction):
        return self.walls[position][direction]
