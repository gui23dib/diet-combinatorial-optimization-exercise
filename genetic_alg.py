from classes.population import PopulationClass
from classes.chromossome import ChromosomeClass
from utils import print_stats
import random

def gen_alg():
    def fitness(population: list[ChromosomeClass], obj: list[int]) -> list[ChromosomeClass]:
        for chromossome in population:
            points = 0
            for i, gene in enumerate(chromossome.value):
                diff = obj[i] - gene
                points += diff ** 2

            chromossome.fitness = 1 / (1 + points) 
        return population

    def mating_pool_roulette(population: list[ChromosomeClass]):
        total_net_fitness = sum([chromosome.fitness for chromosome in population])
        result = random.choices(population, weights=[chromosome.fitness / total_net_fitness for chromosome in population], k=2)

        pointer: int = random.randint(1, len(result[0].value) - 1)
        result[0] = result[0].reproduce(result[1], pointer)
        result[1] = result[1].reproduce(result[0], pointer)

        return result

    def new_generation(population: list[ChromosomeClass], n_survivors: int = 2) -> list[ChromosomeClass]:
        return sorted(population, key=lambda x: x.fitness, reverse=True)[:n_survivors]


    if True:
        try:
            word_obj: str = str(input()).upper()
            objective = [ord(e) for e in word_obj]

            max_iterations: int = 1000000
            gen_count: int = 0

            population: PopulationClass = PopulationClass()
            population.populate(len(objective), len(word_obj) * 10, 100)

            while population.best_fitness != 1.0 and gen_count <= max_iterations:
                population.population = fitness(population.population, objective)
                population.sort_population() # sort population by fitness (already defines the best fitness)

                print_stats(population, gen_count)

                new_population: list[ChromosomeClass] = new_generation(population.population, 2)
                while len(new_population) < len(population.population):
                    for child in mating_pool_roulette(population.population): # pick your mating pool method here
                        new_population.append(ChromosomeClass(child.mutate()))

                population.population = new_population
                gen_count += 1
        except KeyboardInterrupt:
            print("Process interrupted by user")
        except EOFError:
            print("No input given")

        print("All generations have been processed.")
        print(f"Total generations: {gen_count}")
        print(f"Best chromosome: {[chr(e) for e in population.population[0].value]} {population.best_fitness}", end="")

de

if __name__ == '__main__':
    gen_alg()