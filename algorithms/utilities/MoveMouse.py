class MoveMouse:

    def __init__(self):
        self.curr_position = (0, 0)
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors = {
            self.NORTH: (0, 1),
            self.EAST: (1, 0),
            self.SOUTH: (0, -1),
            self.WEST: (-1, 0)
        }
        self.orientation = self.NORTH
        self.start_position = (0, 0)
        self.turns = 0
        self.path = []
        self.tot_t = 0


    def move_update_position(self, direction):
        if direction == self.orientation:
            self.turns += 0
        elif direction == (self.orientation + 2) % 4:
            self.turns += 2
        else:
            self.turns += 1
        dx, dy = self.directionVectors[direction]
        self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)
        self.path.append(self.curr_position)
        self.orientation = direction

    def reset_env(self):
        self.curr_position = self.start_position
        self.orientation = self.NORTH
        self.turns = 0
        self.path = []
        self.tot_t = 0

    def get_stats(self):
        path_length = len(self.path)
        # Todo: add time taken to run, memory usage
        return path_length, self.turns
    
    def get_path(self):
        return self.path

