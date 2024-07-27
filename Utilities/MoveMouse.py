from Utilities import API
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

    def turn_right(self):
        API.turnRight()
        self.orientation = (self.orientation + 1) % 4

    def turn_left(self):
        API.turnLeft()
        self.orientation = (self.orientation - 1) % 4

    def turn_around(self):
        API.turnLeft()
        API.turnLeft()
        self.orientation = (self.orientation + 2) % 4

    def turn_to_direction(self, direction):
        if (self.orientation + 1) % 4 == direction:
            self.turn_right()
        elif (self.orientation - 1) % 4 == direction:
            self.turn_left()
        elif (self.orientation + 2) % 4 == direction:
            self.turn_around()

    def move_update_position(self, direction):
        if direction != self.orientation:
            self.turn_to_direction(direction)
        API.moveForward()
        dx, dy = self.directionVectors[self.orientation]
        self.curr_position = (self.curr_position[0] + dx, self.curr_position[1] + dy)

    def move(self, directions):
        # ToDo: refactor
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
        elif (self.orientation + 2) % 4 in directions:
            self.move_update_position((self.orientation + 2) % 4)
        else:
            pass
