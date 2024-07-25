import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Helper_Classes import API, MoveMouse, Walls
import sys
import random
from collections import deque
import pickle
import json

class FloodFill(MoveMouse):
    def __init__(self):
        super().__init__()
        self.mazeWidth = 16
        self.mazeHeight = 16
        self.positions = [(n, m) for n in range(self.mazeWidth) for m in range(self.mazeHeight)]
        self.walls = {a: [False, False, False, False] for a in self.positions}
        self.visited_cells = {a: False for a in self.positions}
        inf = 100000
        self.flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        self.found_shortest = False
        self.start_position = (0,0)
        self.goal_position = None
        self.walls[self.start_position] = [False, False, True,False]

    def update_walls(self):
        if self.visited_cells[self.curr_position]:
            return

        self.visited_cells[self.curr_position] = True
        API.setColor(self.curr_position[0], self.curr_position[1], 'g')

        if self.orientation == self.NORTH:
            north = bool(API.wallFront())
            east = bool(API.wallRight())
            west = bool(API.wallLeft())
            south = self.walls[self.curr_position][self.SOUTH]
        elif self.orientation == self.EAST:
            north = bool(API.wallLeft())
            east = bool(API.wallFront())
            west = self.walls[self.curr_position][self.WEST]
            south = bool(API.wallRight())
        elif self.orientation == self.SOUTH:
            north = self.walls[self.curr_position][self.NORTH]
            east = bool(API.wallLeft())
            west = bool(API.wallRight())
            south = bool(API.wallFront())
        elif self.orientation == self.WEST:
            north = bool(API.wallRight())
            east = self.walls[self.curr_position][self.EAST]
            west = bool(API.wallFront())
            south = bool(API.wallLeft())

        self.walls[self.curr_position] = [north, east, south, west]
        self.update_walls_neighbors(north, east, south, west)

    def update_walls_neighbors(self, north, east, south, west):
        x, y = self.curr_position

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

    def get_goal_position(self):
        center_x, center_y = self.mazeWidth // 2, self.mazeHeight // 2
        return [(center_x, center_y), (center_x-1, center_y), (center_x, center_y-1), (center_x-1, center_y-1)]

    def is_goal_position(self):
        return self.curr_position in self.get_goal_position()

    def wall_between(self, position, direction):
        return self.walls[position][direction]

    def find_neighbor_descending(self, flood_map = None):
        neighbors = []
        if not flood_map:
            flood_map = self.flood_map

        current_value = flood_map[self.curr_position[0]][self.curr_position[1]]
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = self.curr_position[0] + dx, self.curr_position[1] + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbor_value = flood_map[nx][ny]
                if neighbor_value < current_value and not self.wall_between(self.curr_position, direction):
                    neighbors.append((direction, neighbor_value))

        neighbors.sort(key=lambda x: x[1])
        return neighbors

    def get_flood_value(self, position, flood_map):
        return flood_map[position[0]][position[1]]

    def is_found_shortest(self):
        return self.found_shortest
    
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
        elif (self.orientation + 2) % 4 in directions:
            self.move_update_position((self.orientation + 2) % 4)
        else:
            pass

    def update_text_floodmap(self):
        for i, row in enumerate(self.flood_map):
            for j, val in enumerate(row):
                API.setText(i, j, self.flood_map[i][j])        

    def move_and_floodfill(self, ensure_shortest = True):
        while not self.found_shortest:
            self.update_walls()
            self.update_text_floodmap()
            neighbors_desc = self.find_neighbor_descending()
            if self.is_goal_position():
                self.found_shortest = True
                break

            if not neighbors_desc:
                self.flood_map = self.flood_fill(self.get_goal_position())  # Use the returned flood map

                self.move_and_floodfill()

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            if self.NORTH in directions:
                if not self.wall_between(self.curr_position, self.NORTH):
                    self.move_update_position(self.NORTH)
                else:
                    self.move_and_floodfill()
            elif self.EAST in directions and self.WEST in directions:
                rand_direction = random.choice([self.EAST, self.WEST])
                self.move_update_position(rand_direction)
            elif self.EAST in directions:
                if not self.wall_between(self.curr_position, self.EAST): 
                    self.move_update_position(self.EAST)
                else:
                    self.move_and_floodfill()
            elif self.WEST in directions:
                self.move_update_position(self.WEST)
            elif self.SOUTH in directions:
                self.move_update_position(self.SOUTH)
            else:
                break
                
            if not self.goal_position and self.curr_position in self.get_goal_position():
                self.goal_position = self.curr_position

        if ensure_shortest:
            self.ensure_shortest_path()
        

    def flood_fill(self, goal_positions):
        inf = self.mazeHeight * self.mazeWidth
        local_flood_map = [[inf for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        queue = deque(tuple(goal_positions))
        visited = set(goal_positions)
        
        if isinstance(goal_positions, tuple):
            local_flood_map[goal_positions[0]][goal_positions[1]] = 0
        else:
            for pos in goal_positions:
                local_flood_map[pos[0]][pos[1]] = 0
        n = 1
        while queue:
            # log(queue)
            if isinstance(goal_positions, tuple) and n == 1:
                x = queue.popleft()
                y = queue.popleft()
                n = 2
            else: 
                x, y = queue.popleft()

            current_distance = local_flood_map[x][y]

            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                    if not self.wall_between((x, y), direction) and local_flood_map[nx][ny] > current_distance + 1:
                        local_flood_map[nx][ny] = current_distance + 1
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))
                            visited.add((nx, ny))

        return local_flood_map

    def ensure_shortest_path(self):
        nearest_undiscovered = self.find_nearest_undiscovered()
        if nearest_undiscovered:
            # log(f'Movng to: {nearest_undiscovered}')
            self.move_to_position(nearest_undiscovered)
            self.move_and_floodfill()
        
        self.flood_map = self.flood_fill(self.get_goal_position())
        self.update_text_floodmap()
        
        

    def move_to_position(self, position, go_back_start = False, take_shortest_path = False):
        while not self.curr_position == position:
            current_x, current_y = self.curr_position
            target_x, target_y = position
            
            # if go_back_start:
            #     API.setColor(current_x, current_y, 'b')
            
            if take_shortest_path:
                API.setColor(current_x, current_y, 'r')
            
            flood_map = self.flood_fill(position)
            curr = self.curr_position if self.curr_position else 'F'
            self.update_walls()
            neighbors_desc = self.find_neighbor_descending(flood_map)

            if not neighbors_desc:
                break

            directions = [neighbors_desc[i][0] for i in range(len(neighbors_desc))]
            self.move(directions)

    def go_back_to_start(self):
        self.move_to_position(self.start_position, go_back_start= True)

    def take_shortest_path(self):
        self.move_and_floodfill()

    def find_neighbors(self, position):
        neighbors = []
        x = position[0]
        y = position[1]
        for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
            dx, dy = self.directionVectors[direction]
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                neighbors.append(neighbor)
        
        return neighbors


    def find_nearest_undiscovered(self):
        queue = deque([self.curr_position])
        visited = set([self.curr_position])

        # TODO: early stopping on BFS 

        while queue:
            x, y = queue.popleft()
            for direction in [self.NORTH, self.EAST, self.SOUTH, self.WEST]:
                dx, dy = self.directionVectors[direction]
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:
                    if neighbor not in visited:
                        if not self.visited_cells[neighbor]:
                            neighbors = self.find_neighbors(neighbor)
                            for val in neighbors:
                                if not self.visited_cells[val]: 
                                    log(neighbor)
                                    return neighbor
                        
                        queue.append(neighbor)
                        visited.add(neighbor)
                        self.visited_cells[neighbor] = True
        log('no found')
        return None

    def take_shortest_path(self):
        self.move_to_position(self.goal_position, take_shortest_path=True)

    def save_walls_as_json(self, filename='walls.json'):
        with open(filename, 'w') as file:
            json.dump(self.walls, file)

    # Load the dictionary from a file
    def load_walls_from_json(self, filename='walls.json'):
        with open(filename, 'r') as file:
            self.walls = json.load(file)



def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running floodfill algorithm...")

    exp = FloodFill()
    exp.move_and_floodfill()
    # exp.update_text_floodmap()
    exp.go_back_to_start()
    exp.take_shortest_path()
    exp.save_walls_as_json()
    log(exp.flood_map)

    # goal_positions = exp.get_goal_position()
    # flood_map = exp.flood_fill(goal_positions)  # Get the flood map for navigation
    # log('\nFlood map for navigation:')
    # for row in flood_map:
    #     log(row)

if __name__ == "__main__":
    main()