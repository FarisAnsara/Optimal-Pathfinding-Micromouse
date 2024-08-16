from algorithms.mms_integration import API
import random


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

    def turn_right(self, offline):
        if not offline:
            API.turnRight()
        self.orientation = (self.orientation + 1) % 4

    def turn_left(self, offline):
        if not offline:
            API.turnLeft()
        self.orientation = (self.orientation - 1) % 4

    def turn_around(self, offline):
        if not offline:
            API.turnLeft()
            API.turnLeft()
        self.orientation = (self.orientation + 2) % 4

    def turn_to_direction(self, direction, offline):
        if (self.orientation + 1) % 4 == direction:
            self.turn_right(offline)
        elif (self.orientation - 1) % 4 == direction:
            self.turn_left(offline)
        elif (self.orientation + 2) % 4 == direction:
            self.turn_around(offline)

    def move_update_position(self, direction, offline = False):
        if direction != self.orientation:
            self.turn_to_direction(direction, offline)
        if not offline:
            API.moveForward()
        dx, dy = self.directionVectors[self.orientation]
        self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)

    def move(self, directions):
        if self.orientation in directions:
            self.move_update_position(self.orientation)
        elif (self.orientation + 1) % 4 in directions:
            if (self.orientation - 1) % 4 in directions:
                rand_direction = random.choice([(self.orientation + 1) % 4, (self.orientation - 1) % 4])
                self.move_update_position(rand_direction)
            else:
                self.move_update_position((self.orientation + 1) % 4)
        elif (self.orientation - 1) % 4 in directions:
            self.move_update_position((self.orientation - 1) % 4)
        else:
            self.move_update_position((self.orientation + 2) % 4)

    def reset_env(self):
        API.ackReset()
        self.curr_position = self.start_position
        self.orientation = self.NORTH
