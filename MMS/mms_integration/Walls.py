import time
from MMS.mms_integration import API


class Walls:

    def __init__(self, maze_width, maze_height):
        self.mazeWidth = maze_width
        self.mazeHeight = maze_height
        self.positions = [(n, m) for n in range(self.mazeWidth) for m in range(self.mazeHeight)]
        self.walls = {a: [False, False, False, False] for a in self.positions}
        self.visited_cells = {a: False for a in self.positions}
        self.start_position = (0, 0)
        self.walls[self.start_position] = [False, False, True, True]
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1),
            self.EAST: (1, 0),
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }

        for x in range(16):
            self.walls[(0, x)][self.WEST] = True
            self.walls[(x, 0)][self.SOUTH] = True
            self.walls[(15, x)][self.EAST] = True
            self.walls[(x, 15)][self.NORTH] = True
        time.sleep(2)

    def update_walls(self, position, orientation):
        if self.visited_cells[position]:
            return

        self.visited_cells[position] = True
        API.setColor(position[0], position[1], 'g')

        if orientation == self.NORTH:
            north = bool(API.wallFront())
            east = bool(API.wallRight())
            west = bool(API.wallLeft())
            south = self.walls[position][self.SOUTH]
        elif orientation == self.EAST:
            north = bool(API.wallLeft())
            east = bool(API.wallFront())
            west = self.walls[position][self.WEST]
            south = bool(API.wallRight())
        elif orientation == self.SOUTH:
            north = self.walls[position][self.NORTH]
            east = bool(API.wallLeft())
            west = bool(API.wallRight())
            south = bool(API.wallFront())
        elif orientation == self.WEST:
            north = bool(API.wallRight())
            east = self.walls[position][self.EAST]
            west = bool(API.wallFront())
            south = bool(API.wallLeft())

        self.walls[position] = [north, east, south, west]
        self.update_walls_neighbors(north, east, south, west, position)

    def update_walls_neighbors(self, north, east, south, west, position):
        x, y = position

        neighbors = {
            self.NORTH: (x, y + 1),
            self.EAST: (x + 1, y),
            self.SOUTH: (x, y - 1),
            self.WEST: (x - 1, y)
        }

        if 0 <= neighbors[self.NORTH][0] < self.mazeWidth and 0 <= neighbors[self.NORTH][1] < self.mazeHeight:
            self.walls[neighbors[self.NORTH]][2] = north

        if 0 <= neighbors[self.EAST][0] < self.mazeWidth and 0 <= neighbors[self.EAST][1] < self.mazeHeight:
            self.walls[neighbors[self.EAST]][3] = east

        if 0 <= neighbors[self.SOUTH][0] < self.mazeWidth and 0 <= neighbors[self.SOUTH][1] < self.mazeHeight:
            self.walls[neighbors[self.SOUTH]][0] = south

        if 0 <= neighbors[self.WEST][0] < self.mazeWidth and 0 <= neighbors[self.WEST][1] < self.mazeHeight:
            self.walls[neighbors[self.WEST]][1] = west

    def wall_between(self, position, direction):
        return self.walls[position][direction]
