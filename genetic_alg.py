from classes.food import FoodNode
from classes.nutrition_dataframe import NutritionDataFrame
from data.tools.utils import print_stats
from genetic_alg.population import PopulationClass
from genetic_alg.chromossome import ChromosomeClass
import random

class GeneticAlgorithmOptimization:
    def __init__(
            self, 
            dataframe: list[FoodNode], 
            objective: tuple[int, int], 
            mutation_rate: float = 0.05,
            max_iterations: int = 10000,
            solution_size: int = 10,
            population_length: int = 100,
        ):
        self.dataframe: list[FoodNode] = dataframe
        self.objective: tuple[int, int] = objective
        
        self.popclass: PopulationClass = PopulationClass()
        self.popclass.populate(solution_size, population_length, len(dataframe) - 1)
        
        self.population: list[ChromosomeClass] = self.popclass.population
        
        self.solution_size = solution_size
        self.population_length = population_length
        self.mutation_rate = mutation_rate
        self.max_iterations: int = max_iterations
        
    def fitness(self, obj: tuple[int, int]) -> list[ChromosomeClass]:
        for chromossome in self.population:
            total_protein = 0
            total_calories = 0
            for _, gene in enumerate(chromossome.value):
                total_calories += int(self.dataframe[gene].calories)
                total_protein += int(self.dataframe[gene].protein)
            
            if total_calories > obj[0]:  # obj[0] is the maximum allowed calories
                chromossome.fitness = 0
            else:
                chromossome.fitness = total_protein  # Fitness is the total protein
        return self.population

    def mating_pool_roulette(self):
        total_net_fitness = sum([chromosome.fitness for chromosome in self.population])
        result = random.choices(self.population, weights=[chromosome.fitness / total_net_fitness for chromosome in self.population], k=2)

        pointer: int = random.randint(1, len(result[0].value) - 1)
        result[0] = result[0].reproduce(result[1], pointer)
        result[1] = result[1].reproduce(result[0], pointer)

        return result

    def new_generation(self, n_survivors: int = 2) -> list[ChromosomeClass]:
        return sorted(self.population, key=lambda x: x.fitness, reverse=True)[:n_survivors]

    def run(self) -> int:
        try:
            gen_count: int = 0

            while self.popclass.best_fitness != 1.0 and gen_count <= self.max_iterations:
                self.population = self.fitness(self.objective)
                self.popclass.sort_population() # sort population by fitness (already defines the best fitness)

                print_stats(self.population, gen_count)

                new_population: list[ChromosomeClass] = self.new_generation()
                while len(new_population) < len(self.population):
                    for child in self.mating_pool_roulette(): # pick your mating pool method here
                        new_population.append(ChromosomeClass(child.mutate(self.mutation_rate, len(self.dataframe) - 1)))

                self.population = new_population
                gen_count += 1
        except KeyboardInterrupt:
            print("Process interrupted by user")
        except EOFError:
            print("No input given")

        print("All generations have been processed.")
        print(f"Total generations: {gen_count}")
        print(f"Best chromosome: {[e for e in self.population[0].value]} {self.best_fitness}", end="\n")
        suma = 0
        for item in self.population[0].value:
            x = self.dataframe[item]
            print(x.name, x.calories, x.protein)
            suma += int(x.calories)
        print(f"CALORIAS FINAIS: {suma}\n")
        
        return suma

if __name__ == '__main__':
    data = NutritionDataFrame()

    ga = GeneticAlgorithmOptimization(
        solution_size=10, 
        population_length=100, 
        dataframe=data.foodlist,
        objective=(2000, 200)
    )
    
    res = ga.run()
