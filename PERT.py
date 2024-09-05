import networkx as nx
import matplotlib.pyplot as plt
import math as mat
# Function to calculate expected time
def calculate_expected_time(O, M, P):
    return (O + 4 * M + P) / 6

# Function to calculate variance
def calculate_variance(O, P):
    return ((P - O) / 6) ** 2

# Get the number of activities
num_activities = int(input("Enter the number of activities: "))

# Define the activities dictionary
activities = {}
variances = {}
dependencies = {}

# Input activity details
dep_type = input(f"Will the dependencies for be (P)redecessors or (S)uccessors? ").strip().upper()
for _ in range(num_activities):
    name = input("Enter the activity name: ")
    O = float(input(f"Enter the Optimistic time for {name}: "))
    M = float(input(f"Enter the Most likely time for {name}: "))
    P = float(input(f"Enter the Pessimistic time for {name}: "))
    
    # Calculate expected time and variance
    Tex = calculate_expected_time(O, M, P)
    var = calculate_variance(O, P)
    
    activities[name] = Tex
    variances[name] = var
    
    # Ask if dependencies are predecessors or successors
    
    
    # Input dependencies
    deps = input(f"Enter the dependencies for {name} (comma-separated), or leave empty if none: ")
    if deps:
        dependencies[name] = (deps.split(','), dep_type)
    else:
        dependencies[name] = ([], dep_type)

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for activity in activities:
    G.add_node(activity, weight=activities[activity])

# Add edges with weights based on dependency type
for activity, (deps, dep_type) in dependencies.items():
    for dep in deps:
        dep = dep.strip()
        if dep_type == 'P':  # If dependencies are predecessors
            G.add_edge(dep, activity, weight=activities[activity])
        elif dep_type == 'S':  # If dependencies are successors
            G.add_edge(activity, dep, weight=activities[dep])

# Find all paths from start nodes to end nodes
all_paths = []
for start_node in G.nodes():
    for end_node in G.nodes():
        if start_node != end_node:
            all_paths += list(nx.all_simple_paths(G, source=start_node, target=end_node))

# Calculate the duration of each path
path_durations = []
for path in all_paths:
    duration = sum(G.nodes[activity]['weight'] for activity in path)
    path_durations.append((path, duration))

# Find the critical path
critical_path, critical_duration = max(path_durations, key=lambda x: x[1])

# Calculate the variance for the critical path
critical_path_variance = sum(variances[activity] for activity in critical_path)
sigma=mat.sqrt(critical_path_variance)

# Print the critical path, its duration, and variance
print("\nCritical Path:", " -> ".join(critical_path))
print("Critical Duration:", critical_duration)
print("Critical Path Variance:", critical_path_variance)
print("Critical Path sigma:", sigma)

numberOfIt = int(input("Enter the amount of days you will be using to calculate : "))

times = []

for i in range(numberOfIt):
    timeInput = float(input("Enter the number to calculate : "))
    times.append(timeInput)  # Use append() to add elements to the end

for time in times:
    Zvalue = (time - critical_duration) / sigma
    print("The Z value for time {} is {}".format(time, Zvalue))

#Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
