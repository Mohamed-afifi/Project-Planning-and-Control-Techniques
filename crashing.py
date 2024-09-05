from collections import defaultdict, deque

# Define the activities
activities = {
    "A": {"duration": 8, "cost": 325, "crashed_duration": 5, "crashed_cost": 400, "predecessors": []},
    "B": {"duration": 12, "cost": 1200, "crashed_duration": 11, "crashed_cost": 1320, "predecessors": []},
    "C": {"duration": 17, "cost": 900, "crashed_duration": 14, "crashed_cost": 1020, "predecessors": []},
    "D": {"duration": 7, "cost": 520, "crashed_duration": 5, "crashed_cost": 600, "predecessors": ["A"]},
    "E": {"duration": 5, "cost": 210, "crashed_duration": 4, "crashed_cost": 270, "predecessors": ["B", "D"]},
    "F": {"duration": 8, "cost": 100, "crashed_duration": 7, "crashed_cost": 190, "predecessors": ["B"]},
    "G": {"duration": 5, "cost": 200, "crashed_duration": 4, "crashed_cost": 250, "predecessors": ["E"]},
    "H": {"duration": 3, "cost": 300, "crashed_duration": 2, "crashed_cost": 400, "predecessors": ["C", "F"]}
}

# Create a graph from the activities
graph = defaultdict(list)
in_degree = defaultdict(int)
for activity, details in activities.items():
    in_degree[activity] = len(details["predecessors"])
    for predecessor in details["predecessors"]:
        graph[predecessor].append(activity)

# Perform a topological sort using Kahn's algorithm
def topological_sort(graph, in_degree):
    zero_in_degree = deque([node for node in graph if in_degree[node] == 0])
    sorted_list = []
    
    while zero_in_degree:
        node = zero_in_degree.popleft()
        sorted_list.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)
                
    return sorted_list

# Find the longest path in the graph using topological order
def find_critical_path(sorted_list, activities):
    start_times = {node: 0 for node in sorted_list}
    end_times = {node: 0 for node in sorted_list}
    for node in sorted_list:
        end_times[node] = start_times[node] + activities[node]["duration"]
        for neighbor in graph[node]:
            if end_times[node] > start_times[neighbor]:
                start_times[neighbor] = end_times[node]
    
    # Find the end time of the last activity
    last_activity = sorted_list[-1]
    critical_path_end_time = end_times[last_activity]

    # Trace back the critical path
    critical_path = []
    def trace_path(node):
        if not graph[node]:  # If no successors, it's a critical path activity
            critical_path.append(node)
            return
        for neighbor in graph[node]:
            if end_times[node] == start_times[neighbor]:  # It's on the critical path
                trace_path(neighbor)
                critical_path.append(node)
    
    trace_path(last_activity)
    
    return critical_path[::-1], critical_path_end_time

# Execute the algorithm
sorted_list = topological_sort(graph, in_degree)
critical_path, critical_path_end_time = find_critical_path(sorted_list, activities)

print("Critical Path:", critical_path)
print("Critical Path Duration:", critical_path_end_time)
