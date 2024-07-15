

class DynaQ:
    def __init__(self, walls, visited_cells, mazeWidth, mazeHeight):
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1), 
            self.EAST: (1, 0), 
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }

        self.curr_position = (0, 0)
        self.q_table = {}
        self.positions = [(n, m) for n in range(self.mazeWidth) for m in range(self.mazeHeight)]
        for position in self.positions:
            self.q_table[position] = [0, 0, 0, 0]
            
        self.walls = walls
        self.visited_cells = visited_cells

        inf = 100000
        self.flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]

        self.orientation = self.NORTH
        self.start_position = (0,0)
        self.goal_position = None


    