from classes.ant import AntClass
import random

class AntPopulation:
    population: list[AntClass] = []
    best_fitness: float = -1.0
    
    def __init__(self):
        pass

    def populate(self, population_length: int, id_range: int) -> list[AntClass]:
        if self.population is None or self.population == []:
            for _ in range(population_length):
                self.population.append(AntClass(starting_point=random.randint(0, id_range)))
    
        return self.population

    def sort_population(self) -> list[AntClass]:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.population[0].fitness # best fitness is the first element of the sorted list
        return self.population