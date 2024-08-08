from Utilities import API


class Utils:

    def __init__(self, maze_width=16, maze_height=16):
        self.mazeWidth = maze_width
        self.mazeHeight = maze_height

    def get_goal_position(self):
        center_x, center_y = self.mazeWidth // 2, self.mazeHeight // 2
        return [(center_x, center_y), (center_x - 1, center_y), (center_x, center_y - 1), (center_x - 1, center_y - 1)]

    def is_goal_position(self, position):
        return position in self.get_goal_position()

    @staticmethod
    def get_flood_value(position, flood_map):
        return flood_map[position[0]][position[1]]

    @staticmethod
    def update_text_flood_map(flood_map):
        for i, row in enumerate(flood_map):
            for j, val in enumerate(row):
                API.setText(i, j, flood_map[i][j])
