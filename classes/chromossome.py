import random

class ChromosomeClass:
    def __init__(self, value, fitness = -1):
        self.value = value # group of genes
        self.fitness: float = fitness # fitness value
    
    def reproduce(self, other, crossover_point: int):
        return ChromosomeClass(self.value[:crossover_point] + other.value[crossover_point:])

    def mutate(self, mutation_rate: float = 0.05):
        for i in range(len(self.value)):
            if random.random() < mutation_rate:
                new_gene = random.randint(65, 90)

                while self.value[i] == new_gene: # avoid gene repetition
                    new_gene = random.randint(65, 90)

                self.value[i] = new_gene

        return self.value