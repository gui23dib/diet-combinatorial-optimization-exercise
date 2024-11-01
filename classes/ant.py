import random

class AntClass:
    def __init__(self, starting_point: int, tour_path: list[int] = [], visited: list[int] = []):
        self.tour_path: list[int] = tour_path or [starting_point]
        self.visited: list[int] = visited or [starting_point]
        self.starting_point: int = starting_point
        self.fitness: float = 0.0
        
    
        
class AntPopulation:
    population: list[AntClass] = []
    best_fitness: float = -1.0
    
    def __init__(self):
        pass

    def populate(self, population_length: int, id_range: int) -> list[AntClass]:
        if self.population is None or self.population == []:
            for _ in range(population_length):
                temp: int = random.randint(1, id_range)
                self.population.append(AntClass(temp))
    
        return self.population

    def sort_population(self) -> list[AntClass]:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.population[0].fitness # best fitness is the first element of the sorted list
        return self.population
    