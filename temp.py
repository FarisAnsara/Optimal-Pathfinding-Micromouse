import numpy as np
import matplotlib.pyplot as plt

# Define the maze dimensions and the walls
maze_size = 8
maze = np.zeros((maze_size, maze_size))

# Adding walls (1 represents a wall)
walls = [
    (1, 0), (1, 1), (1, 2), (3, 1), (4, 1), (4, 2), (5, 2), 
    (6, 2), (6, 3), (6, 4), (6, 5), (4, 5), (2, 4), (2, 5), (3, 4)
]
for wall in walls:
    maze[wall] = 1

# Define BFS pathfinding function
def bfs(maze, start, goal):
    rows, cols = maze.shape
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        (current, path) = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            return path
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_node = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_node[0] < rows and 0 <= next_node[1] < cols and maze[next_node] == 0:
                queue.append((next_node, path + [next_node]))
    return []

# Define start and goal positions
start = (0, 0)
goal = (7, 7)

# Find the path using BFS
path = bfs(maze, start, goal)

# Plot the maze and the path
plt.figure(figsize=(8, 8))
plt.imshow(maze, cmap="gray_r")

# Plot the BFS path
for idx, (x, y) in enumerate(path):
    plt.text(y, x, str(idx), ha='center', va='center', color='blue')

plt.xticks(range(maze_size))
plt.yticks(range(maze_size))
plt.grid(True)
plt.title("8x8 Maze with BFS Pathfinding")

# Save the figure
# plt.savefig("/mnt/data/8x8_maze_with_BFS_pathfinding.png")
plt.show()
