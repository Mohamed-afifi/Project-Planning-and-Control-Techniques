class Activity:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.predecessors = []
        self.successors = []
        self.es = 0  # Earliest Start
        self.ef = 0  # Earliest Finish
        self.ls = float('inf')  # Latest Start
        self.lf = float('inf')  # Latest Finish
        self.float = 0  # Float Time

    def calculate_early_times(self):
        if not self.predecessors:
            self.es = 0
        else:
            self.es = max(pre.ef for pre in self.predecessors)
        self.ef = self.es + self.duration

    def calculate_late_times(self):
        if not self.successors:
            self.lf = self.ef
        else:
            self.lf = min(succ.ls for succ in self.successors)
        self.ls = self.lf - self.duration
        self.float = self.ls - self.es

    def is_critical(self):
        return self.float == 0

def find_critical_path(activities):
    # Perform forward pass to calculate ES and EF
    for activity in activities.values():
        activity.calculate_early_times()

    # Perform backward pass to calculate LS and LF
    for activity in reversed(list(activities.values())):
        activity.calculate_late_times()

    # Identify the critical path
    critical_path = []
    current_activity = max(activities.values(), key=lambda x: x.ef)
    while current_activity:
        critical_path.append(current_activity.name)
        next_activity = None
        for pre in current_activity.predecessors:
            if pre.ef == current_activity.es:
                next_activity = pre
                break
        current_activity = next_activity

    return list(reversed(critical_path))

def input_activities():
    activities = {}
    num_activities = int(input("Enter the number of activities: "))

    for i in range(num_activities):
        name = input(f"Enter the name of activity {i+1}: ")
        duration = int(input(f"Enter the duration of activity {name}: "))
        activities[name] = Activity(name, duration)

    dependency_type = input("Will you enter successors or predecessors? (Enter 'S' for successors, 'P' for predecessors): ").strip().upper()

    if dependency_type == 'S':
        for activity in activities.values():
            successors = input(f"Enter the successors of activity {activity.name} (comma-separated, leave blank if none): ").strip().split(',')
            activity.successors = [activities[s.strip()] for s in successors if s.strip()]
            for succ in activity.successors:
                succ.predecessors.append(activity)
    elif dependency_type == 'P':
        for activity in activities.values():
            predecessors = input(f"Enter the predecessors of activity {activity.name} (comma-separated, leave blank if none): ").strip().split(',')
            activity.predecessors = [activities[p.strip()] for p in predecessors if p.strip()]
            for pre in activity.predecessors:
                pre.successors.append(activity)

    return activities

# Main function
if __name__ == "__main__":
    activities = input_activities()
    critical_path = find_critical_path(activities)

    # Display the results
    print("\nActivity\tES\tEF\tLS\tLF\tFloat")
    for name, activity in activities.items():
        print(f"{name}\t\t{activity.es}\t{activity.ef}\t{activity.ls}\t{activity.lf}\t{activity.float}")

    print("\nCritical Path:", " -> ".join(critical_path))
