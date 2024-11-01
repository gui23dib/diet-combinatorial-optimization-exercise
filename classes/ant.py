import random

class AntClass:
    def __init__(self, starting_point: int, tour_path: list[int] = [], visited: list[int] = []):
        self.tour_path: list[int] = tour_path or [starting_point]
        self.visited: list[int] = visited or [starting_point]
        self.starting_point: int = starting_point
        self.fitness: float = 0.0
        
    def calculate_tour_length(self, distances: list[list[int]]) -> float:
        total_distance: float = 0.0
        for i in range(len(self.tour_path) - 1):
            total_distance += distances[self.tour_path[i]][self.tour_path[i + 1]]
        
        return total_distance
    
    def calculate_fitness(self, distances: list[list[int]]) -> float:
        self.fitness = 1 / (1 + self.calculate_tour_length(distances))
        return self.fitness
    
    def move(self, pheromone: list[list[float]], distances: list[list[int]], alpha: float, beta: float) -> int:
        current_node: int = self.tour_path[-1]
        unvisited: list[int] = [node for node in range(len(pheromone)) if node not in self.visited]
        
        if not unvisited:
            return -1
        
        probabilities: list[float] = [0.0 for _ in range(len(pheromone))]
        total: float = 0.0
        
        for node in unvisited:
            total += (pheromone[current_node][node] ** alpha) * ((1 / distances[current_node][node]) ** beta)
        
        for node in unvisited:
            probabilities[node] = (pheromone[current_node][node] ** alpha) * ((1 / distances[current_node][node]) ** beta) / total
        
        for i in range(1, len(probabilities)):
            probabilities[i] += probabilities[i - 1]
        
        rand: float = random.random()
        for i in range(len(probabilities)):
            if rand < probabilities[i]:
                return unvisited[i]
        
        return -1
    
    def tour(self, pheromone: list[list[float]], distances: list[list[int]], alpha: float, beta: float) -> list[int]:
        while len(self.tour_path) < len(pheromone):
            move: int = self.move(pheromone, distances, alpha, beta)
            
            if move == -1:
                self.tour_path.append(self.starting_point)
                break
            
            self.tour_path.append(move)
            self.visited.append(move)
        
        return self.tour_path
    
    def reset(self):
        self.tour_path = [self.starting_point]
        self.visited = [self.starting_point]
        self.fitness = 0.0
    