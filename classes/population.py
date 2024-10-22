import random
from classes.chromossome import ChromosomeClass

class PopulationClass:
    population: list[ChromosomeClass] = []
    best_fitness: float = -1.0

    def __init__(self):
        pass

    def populate(self, objective_length: int, population_length: int) -> list[ChromosomeClass]:
        if self.population is None or self.population == []:
            for _ in range(population_length):
                temp = [random.randint(65, 90) for __ in range(objective_length)]
                self.population.append(ChromosomeClass(temp))
                
        return self.population

    def sort_population(self) -> list[ChromosomeClass]:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.population[0].fitness # best fitness is the first element of the sorted list
        return self.population