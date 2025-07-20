# graph.py

import csv

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start_node, end_node, base_time, traffic_factor):
        travel_time = int(base_time) * float(traffic_factor)
        if start_node not in self.adjacency_list:
            self.adjacency_list[start_node] = []
        self.adjacency_list[start_node].append((end_node, travel_time))

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 4:
                    continue
                start, end, base, traffic = row
                self.add_edge(start, end, base, traffic)

    def __str__(self):
        result = "Graph with Traffic:\n"
        for node, edges in self.adjacency_list.items():
            edge_str = ', '.join([f"{dest} ({time:.1f})" for dest, time in edges])
            result += f"{node} -> {edge_str}\n"
        return result
