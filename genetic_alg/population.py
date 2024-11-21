import random

from genetic_alg.chromossome import ChromosomeClass

class PopulationClass:
    population: list[ChromosomeClass] = []
    best_fitness: float = -1.0
    
    def __init__(self):
        pass

    def populate(self, population_length: int, id_range: int, solution_max_size, solution_min_size) -> list[ChromosomeClass]:
        if self.population is None or self.population == []:
            for _ in range(population_length):
                chromosome_size = random.randint(solution_min_size, solution_max_size)
                temp: list[int] = [random.randint(1, id_range) for __ in range(chromosome_size)]
                self.population.append(ChromosomeClass(temp))
                
        return self.population

    def sort_population(self) -> list[ChromosomeClass]:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.population[0].fitness # best fitness is the first element of the sorted list
        return self.population