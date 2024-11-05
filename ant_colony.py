import random

class Ant:
    def __init__(self, nodes, target_value):
        self.nodes = nodes
        self.target_value = target_value
        self.path = []
        self.total = 0

    def walk(self):
        # Reset path and total
        self.path = []
        self.total = 0
        
        # Continue walking until we reach or exceed the target
        while self.total < self.target_value:
            next_node = random.choice(self.nodes)
            self.path.append(next_node)
            self.total += next_node
            
            # Allow breaking if total goes over to avoid endless loops
            if self.total > self.target_value:
                break

class AntColonyOptimizer:
    def __init__(self, nodes, target_value, n_ants, n_iterations, evaporation_rate, pheromone_intensity):
        self.nodes = nodes
        self.target_value = target_value
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        self.pheromone_intensity = pheromone_intensity
        
        # Initialize pheromone levels for each node
        self.pheromones = {node: 1.0 for node in nodes}
        
    def run(self):
        best_path = None
        best_total = float('inf')
        
        for iteration in range(self.n_iterations):
            all_paths = []
            
            # Create ants and let them generate paths
            for _ in range(self.n_ants):
                ant = Ant(self.nodes, self.target_value)
                ant.walk()
                all_paths.append((ant.path, ant.total))
                
                # Update best path if the current path is closer to the target
                if abs(ant.total - self.target_value) < abs(best_total - self.target_value):
                    best_path = ant.path
                    best_total = ant.total

            # Update pheromones based on paths
            self.update_pheromones(all_paths)
            
            print(f"Iteration {iteration + 1}, Best Path: {best_path}, Best Total: {best_total}")
        
        return best_path, best_total

    def update_pheromones(self, paths):
        # Evaporate some pheromone from all nodes
        for node in self.pheromones:
            self.pheromones[node] *= (1 - self.evaporation_rate)
        
        # Add pheromones based on path quality
        for path, total in paths:
            distance_to_target = abs(total - self.target_value)
            if distance_to_target == 0:
                pheromone_deposit = self.pheromone_intensity
            else:
                pheromone_deposit = self.pheromone_intensity / distance_to_target

            for node in path:
                self.pheromones[node] += pheromone_deposit

    def select_next_node(self):
        # Probabilistically choose the next node based on pheromone levels
        pheromone_sum = sum(self.pheromones.values())
        choices = []
        
        for node in self.nodes:
            probability = self.pheromones[node] / pheromone_sum
            choices.append((node, probability))
        
        # Weighted random choice
        return random.choices([node for node, _ in choices], weights=[prob for _, prob in choices])[0]


# Parameters for the ACO algorithm
nodes = [1, 2, 3, 5, 8]  # Possible steps (nodes) for ants
target_value = 15        # Target integer value to reach
n_ants = 10               # Number of ants per iteration
n_iterations = 20         # Number of iterations
evaporation_rate = 0.1    # Pheromone evaporation rate
pheromone_intensity = 100 # Intensity of pheromone deposit

# Run the ACO algorithm
aco = AntColonyOptimizer(nodes, target_value, n_ants, n_iterations, evaporation_rate, pheromone_intensity)
best_path, best_total = aco.run()
print(f"Best path found: {best_path} with total {best_total}")
