# Optimal Pathfinding and Execution Strategies for Micromouse Maze Navigation

## Description

This repository was created as part of my master's dissertation, **"Optimal Pathfinding and Execution Strategies for Micromouse Maze Navigation."** It contains various classical and reinforcement learning (RL) algorithms designed to solve mazes autonomously, simulating the behavior of a micromouse.

A micromouse is a small autonomous robot that aims to navigate from a starting position to one or more preset goal positions within a maze. The goal of this research is to evaluate and compare the performance of different algorithms in navigating through mazes, considering factors such as path time, number of turns, distance traveled, and execution time.

The algorithms implemented in this study are split into two categories: **Classical** and **Reinforcement Learning (RL)** algorithms.

### Classical Algorithms:
- Breadth-First Search (BFS)
- A* Search
- Dijkstra’s Algorithm
- FloodFill

### Reinforcement Learning (RL) Algorithms:
- Q-learning
- SARSA
- Dyna-Q with Q-learning updates
- Dyna-Q with a hybrid of SARSA and Q-learning updates

The classical algorithms were implemented with distance-based approaches, while only FloodFill, BFS, and the two Dyna-Q variants were implemented with time-based approaches.

### Usage

Algorithms can be run in two main ways:
1. Using Jupyter Notebooks:
    - **Data Collection Notebook (DCN)** for collecting results.
    - **Data Manipulation and Visualization Notebook (DMVN)** for analyzing and visualizing the results.
2. Using the **Micromouse Simulator (MMS)** from the MMS repository (https://github.com/mackorone/mms/tree/main).

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.6 or later
- `pip` (Python package installer)
- `git`

### 1. Clone the Repository
```bash
git clone https://github.com/FarisAnsara/Optimal-Pathfinding-Micromouse.git
```

### 2. Clone the MMS Repository
Follow the steps on MMS Repository (https://github.com/mackorone/mms/tree/main) if you want to use the Micromouse Simulator.

## Use with MMS
To run the algorithms on the MMS:

1. Set up the MMS according to the instructions provided on https://github.com/mackorone/mms/tree/main
2. The algorithm code files are found in the ```MMS``` directory of this repository

## Running the Algorithms for Data Collection
All the algorithms are stored in the ```algorithms``` directory, which contains subdirectories for each specific algorithm. To collect data for each algorithm, run the ```DCN.ipynb``` Jupyter Notebook. The notebook handles loading mazes, running algorithms, and storing the results for later analysis. Note that running this notebook is time-consuming as the RL algorithm take a long time.

## Example Usage
Here is an example of how to run the FloodFill algorithm on a set of mazes:

```python
import glob
import json
import os

from algorithms.utilities.Utils import Utils
from algorithms.utilities.Stats import Stats
from algorithms.classical.floodfill.FloodFill import FloodFill
import pandas as pd
import time

maze = Utils.load_maze('mazes/competition_json/alljapan-031-2010-exp-fin.json')

def get_mazes_json(dirname):
    mazes = {}
    for maze_file in glob.glob(os.path.join(dirname, '*.json')):
        with open(maze_file, 'r') as f:
            maze_name = os.path.basename(maze_file).split('.')[0]
            mazes[maze_name] = {eval(k): v for k, v in json.load(f).items()} 
    return mazes

mazes = get_mazes_json('mazes/competition_json')

def get_runtime(start_time):
    end_time = time.perf_counter_ns()
    return end_time - start_time

stats = Stats()
flood_paths = []
flood_path_times = []
flood_turns = []
flood_distances = []
flood_cells_travelled = []
flood_exec_time = []

for name, item in mazes.items():
    start_time = time.perf_counter_ns()
    flood = FloodFill(walls=item)
    flood_exec_time.append(get_runtime(start_time) * pow(10, -3))  # Convert to microseconds
    path = flood.get_path_from_flood_map()
    flood_paths.append(path)
    flood_path_times.append(stats.get_time_from_path(path))
    dist, turns = flood.get_stats()
    flood_cells_travelled.append(dist)
    flood_distances.append(stats.get_dist_travelled())
    flood_turns.append(turns)

# Save the results to a DataFrame and export as CSV
maze_names = mazes.keys()
data = {
    'Maze Name': maze_names,
    'Path': flood_paths,
    'Path Time (s)': flood_path_times,
    'Turns': flood_turns,
    'Distance Travelled (m)': flood_distances,
    'Execution Time (micro secs)': flood_exec_time,
    'Cells Travelled': flood_cells_travelled
}

flood_fill_df = pd.DataFrame(data).set_index('Maze Name')
flood_fill_df.to_csv('results/csv_files/competition/final/flood_fill.csv')
```

This example demonstrates:
1. Loading a set of mazes from JSON files.
2. Running the FloodFill algorithm on each maze.
3. Collecting performance metrics such as execution time, path time, and distance traveled.
4. Saving the results to a CSV file.

## Results and Data Visualization
Once the algorithms have been executed and the data has been collected, you can visualize the results by running the ```DMVN.ipynb``` notebook. This notebook contains code to load the generated CSV files, perform further analysis, and visualize the performance of each algorithm.