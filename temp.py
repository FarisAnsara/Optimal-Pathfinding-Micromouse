stats = Stats()
dynaq_sarsa_paths = []
dynaq_sarsa_path_times = []
dynaq_sarsa_turns = []
dynaq_sarsa_distances = []
dynaq_sarsa_cells_travelled = []
dynaq_sarsa_exec_time = []
dynaq_sarsa_memory = []
for name, item in mazes.items():
    print(f'running {name}')
    start_time = time.perf_counter_ns()
    dynaq_sarsa = dynaq_sarsa(walls=item)
    dynaq_sarsa.run_dynaq_sarsa()
    dynaq_sarsa_exec_time.append(get_runtime(start_time) * pow(10, -3))
    path = dynaq_sarsa.get_path()
    dynaq_sarsa_paths.append(path)
    dynaq_sarsa_path_times.append(stats.get_time_from_path(path))
    dist, turns = dynaq_sarsa.get_stats()
    dynaq_sarsa_cells_travelled.append(dist)
    dynaq_sarsa_distances.append(stats.get_dist_travelled())
    dynaq_sarsa_turns.append(turns)
    dynaq_sarsa_memory.append(dynaq_sarsa.total_memory_used)

maze_names = mazes.keys()

data = {
    'Maze Name': maze_names,
    'Path': dynaq_sarsa_paths,
    'Path Time (s)': dynaq_sarsa_path_times,
    'Turns': dynaq_sarsa_turns,
    'Distance Travelled (m)': dynaq_sarsa_distances,
    'Execution Time (micro secs)': dynaq_sarsa_exec_time,
    'Memory Usage (MB)': dynaq_sarsa_memory,
    'Cells Travelled': astar_cells_travelled
}

dynaq_sarsa_df = pd.DataFrame(data).set_index('Maze Name')
dynaq_sarsa_df.to_csv('results/csv_files/competition/dynaq_sarsa.csv')