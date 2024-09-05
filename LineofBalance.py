import math
import pandas as pd


class Operation:
    def __init__(self, name, man_hours_per_house, optimum_gang_size, target_rate_of_construction):
        self.name = name
        self.man_hours_per_house = man_hours_per_house
        self.optimum_gang_size = optimum_gang_size
        self.target_rate_of_construction = target_rate_of_construction
        self.predecessors = []
        self.successors = []
        self.start_1 = 0
        self.finish_1 = 0
        self.start_n = 0
        self.finish_n = 0
        self.calculate_metrics()

    def calculate_metrics(self):
        # Calculate metrics based on the given parameters
        self.required_men = (self.man_hours_per_house * self.target_rate_of_construction) / (8 * 5)
        self.number_of_gangs = math.ceil(self.required_men / self.optimum_gang_size)
        self.actual_number_of_men = self.number_of_gangs * self.optimum_gang_size
        self.actual_rate_of_construction = self.target_rate_of_construction * (self.actual_number_of_men / self.required_men)
        self.duration_of_one_house = round((self.man_hours_per_house / (self.optimum_gang_size * 8)) * 2) / 2

    def add_predecessor(self, predecessor):
        self.predecessors.append(predecessor)
        predecessor.add_successor(self)

    def add_successor(self, successor):
        self.successors.append(successor)

    def calculate_timing(self, num_units, buffer_size):
        if not self.predecessors:
            # If no predecessors, it's the first operation
            self.start_1 = 0
            self.finish_1 = self.start_1 + self.duration_of_one_house
            self.start_n = self.start_1 + ((num_units - 1) * self.duration_of_one_house) / self.number_of_gangs
            self.finish_n = self.start_n + self.duration_of_one_house
        else:
            # Handle the timing based on the slowest predecessor
            slowest_predecessor = max(self.predecessors, key=lambda pred: pred.finish_n)
            pred_finish_n = slowest_predecessor.finish_n
            pred_finish_1 = slowest_predecessor.finish_1
            pred_rate = slowest_predecessor.actual_rate_of_construction
            curr_rate = self.actual_rate_of_construction

            if curr_rate > pred_rate:
                self.start_n = pred_finish_n + buffer_size
                self.finish_n = self.start_n + self.duration_of_one_house
                self.start_1 = self.start_n - ((num_units - 1) * self.duration_of_one_house) / self.number_of_gangs
                self.finish_1 = self.start_1 + self.duration_of_one_house
            else:
                self.start_1 = pred_finish_1 + buffer_size
                self.finish_1 = self.start_1 + self.duration_of_one_house
                self.start_n = self.start_1 + ((num_units - 1) * self.duration_of_one_house) / self.number_of_gangs
                self.finish_n = self.start_n + self.duration_of_one_house

    def get_timing(self):
        return {
            'Operation': self.name,
            'Man-hours/House': self.man_hours_per_house,
            'Optimum Gang Size': self.optimum_gang_size,
            'Required Men/Week': round(self.required_men, 2),
            'No of Gangs': self.number_of_gangs,
            'Actual No. of Men': self.actual_number_of_men,
            'Actual Rate of Construction': round(self.actual_rate_of_construction, 2),
            'Duration of One House (days)': self.duration_of_one_house,
            'Start OP1_1': round(self.start_1, 2),
            'Finish OP1_1': round(self.finish_1, 2),
            'Start OP1_n': round(self.start_n, 2),
            'Finish OP1_n': round(self.finish_n, 2)
        }


# Example of defining operations and relationships
def main():
    operations = {}
    target_rate_of_construction = 4

    # Define operations with their details (you'll replace these with your real data)
    operations['U'] = Operation('U', 120, 3, target_rate_of_construction)
    operations['V'] = Operation('V', 280, 6, target_rate_of_construction)
    operations['W'] = Operation('W', 250, 4, target_rate_of_construction)
    operations['X'] = Operation('X', 45, 3, target_rate_of_construction)
    operations['Y'] = Operation('Y', 30, 2, target_rate_of_construction)
    operations['Z'] = Operation('Z', 220, 5, target_rate_of_construction)

    # Define relationships (you’ll replace these with the real relationships)
    operations['V'].add_predecessor(operations['U'])
    operations['W'].add_predecessor(operations['V'])
    operations['X'].add_predecessor(operations['W'])
    operations['Y'].add_predecessor(operations['W'])
    operations['Z'].add_predecessor(operations['X'])
    operations['Z'].add_predecessor(operations['Y'])
    
    #operations['Z'].add_predecessor(operations['X'])
    #operations['Z'].add_predecessor(operations['Y'])
    ###OR
    # operations['X'].add_successor(operations['Z'])
    # operations['Y'].add_successor(operations['Z'])

    
    # Calculate timings
    num_units = 40
    buffer_size = 5

    for operation in operations.values():
        operation.calculate_timing(num_units, buffer_size)

    # Store all data in a DataFrame for a nice table output
    data = [operation.get_timing() for operation in operations.values()]
    df = pd.DataFrame(data)
    df.to_excel("LOBresults.xlsx")

    # Display the DataFrame
    print(df)

if __name__ == "__main__":
    main()
