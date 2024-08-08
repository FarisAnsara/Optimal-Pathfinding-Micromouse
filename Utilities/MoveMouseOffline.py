class MoveMouseOffline:

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

    def move_update_position(self, direction):
        dx, dy = self.directionVectors[direction]
        self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)

    def reset_env(self):
        self.curr_position = self.start_position
        self.orientation = self.NORTH
