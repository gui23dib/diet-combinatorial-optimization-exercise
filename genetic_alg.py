from classes.food import FoodNode
from classes.nutrition_dataframe import NutritionDataFrame
from data.tools.utils import print_stats
from genetic_alg.population import PopulationClass
from genetic_alg.chromossome import ChromosomeClass
import random

def fitness(population: list[ChromosomeClass], obj: tuple[int, int], df: list[FoodNode]) -> list[ChromosomeClass]:
    for chromossome in population:
        points = 0
        diff_cal = 0
        for _, gene in enumerate(chromossome.value):
            diff_cal += int(df[gene].calories)
        
        points = abs(obj[0] - diff_cal)

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

def gen_alg(objective: tuple[int, int], dataframe: list[FoodNode]):
    try:
        max_iterations: int = 10000
        solution_size = 10
        population_length = 100
        mutation_rate = 0.05


        gen_count: int = 0

        population: PopulationClass = PopulationClass()
        population.populate(solution_size, population_length, len(dataframe) - 1)

        while population.best_fitness != 1.0 and gen_count <= max_iterations:
            population.population = fitness(population.population, objective, dataframe)
            population.sort_population() # sort population by fitness (already defines the best fitness)

            print_stats(population, gen_count)

            new_population: list[ChromosomeClass] = new_generation(population.population)
            while len(new_population) < len(population.population):
                for child in mating_pool_roulette(population.population): # pick your mating pool method here
                    new_population.append(ChromosomeClass(child.mutate(mutation_rate, len(dataframe) - 1)))

            population.population = new_population
            gen_count += 1
    except KeyboardInterrupt:
        print("Process interrupted by user")
    except EOFError:
        print("No input given")

    print("All generations have been processed.")
    print(f"Total generations: {gen_count}")
    print(f"Best chromosome: {[e for e in population.population[0].value]} {population.best_fitness}", end="\n")
    suma = 0
    for item in population.population[0].value:
        x = dataframe[item]
        print(x.name, x.calories, x.protein)
        suma += int(x.calories)
    print(f"CALORIAS FINAIS: {suma}\n")

if __name__ == '__main__':
    data = NutritionDataFrame()

    obj_kcal = 2000 #utils.get_user_input()

    gen_alg(objective=(obj_kcal,1.0), dataframe=data.foodlist)