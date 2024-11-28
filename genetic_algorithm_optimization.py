from classes.nutrition_dataframe import NutritionDataFrame
from genetic_alg.utils import print_stats
from genetic_alg.population import PopulationClass
from genetic_alg.chromossome import ChromosomeClass
from matplotlib import pyplot as plt
import random

class GeneticAlgorithmOptimization:
    def __init__(
            self, 
            problem: NutritionDataFrame,
            mutation_rate: float = 0.05,
            max_iterations: int = 500,
            population_length: int = 100,
            solution_max_size: int = 25,
            solution_min_size: int = 5,
            elite_size: int = 2,
            convergence_rate: float = 0.5,
            max_portions = 3,
        ):
        self.convergence_rate = convergence_rate
        self.elite_size = elite_size
        self.max_portions = max_portions
        
        self.problem: NutritionDataFrame = problem
        self.popclass: PopulationClass = PopulationClass()
        self.popclass.populate(population_length, len(problem.foodlist) - 1, solution_max_size, solution_min_size)
                
        self.popclass.population_length = population_length
        self.mutation_rate = mutation_rate
        self.max_iterations: int = max_iterations

        self.best_fit_values: list = [] #melhores fit por geração
        self.best_calories_gen: list = [] #melhores calorias por geração
        self.best_macros_gen: list = [] #melhores macros por geração
        
    #Calcula fitness
    def fitness(self) -> list[ChromosomeClass]:
        for chromossome in self.popclass.population:
            gene_count = {}
            reachedMaxPortions = False
            
            for _, gene in enumerate(chromossome.value):
                if gene not in gene_count:
                    gene_count[gene] = 0
                gene_count[gene] += 1
                
                if gene_count[gene] > self.max_portions:
                    reachedMaxPortions = True
                    break

            if reachedMaxPortions:
                chromossome.fitness = 0
            else:
                chromossome.fitness = self.problem.evaluate(chromossome.value)
        return self.popclass.population


    #Roleta Viciada
    def mating_pool_roulette(self):
        total_net_fitness = sum([chromosome.fitness for chromosome in self.popclass.population])
        if(total_net_fitness == 0): return random.choices(self.popclass.population, k=2)
        result = random.choices(self.popclass.population, weights=[chromosome.fitness / total_net_fitness for chromosome in self.popclass.population], k=2)

        pointer: int = random.randint(1, len(result[0].value) - 1)
        
        if random.random() < self.convergence_rate:
            result[0] = result[0].reproduce(result[1], pointer)
            result[1] = result[1].reproduce(result[0], pointer)

        return result

    #Cria uma nova geração ordenada
    def new_generation(self) -> list[ChromosomeClass]:
        return sorted(self.popclass.population, key=lambda x: x.fitness, reverse=True)[:self.elite_size]

    def run(self) -> int:
        try:
            gen_count: int = 0
            
            while self.popclass.best_fitness != 1.0 and gen_count <= self.max_iterations:
                self.popclass.population = self.fitness()
                self.popclass.sort_population() # sort population by fitness (already defines the best fitness)
                self.best_fit_values.append(self.popclass.best_fitness) 
                
                soma_calorias = 0
                soma_prot = 0
                soma_fat = 0
                soma_carbs = 0
                for food in self.popclass.population[0].value:
                    soma_calorias += self.problem.foodlist[food].calories
                    soma_fat += self.problem.foodlist[food].fat
                    soma_carbs += self.problem.foodlist[food].carbs
                    soma_prot += self.problem.foodlist[food].protein
                    
                self.best_calories_gen.append(soma_calorias)
                self.best_macros_gen.append([soma_prot, soma_fat, soma_carbs])

                print_stats(self.popclass, gen_count)

                new_population: list[ChromosomeClass] = self.new_generation()
                while len(new_population) < len(self.popclass.population):
                    for child in self.mating_pool_roulette(): # pick your mating pool method here
                        new_population.append(ChromosomeClass(child.mutate(self.mutation_rate, len(self.problem.foodlist) - 1)))

                self.popclass.population = new_population
                gen_count += 1
        except KeyboardInterrupt:
            print("Process interrupted by user")
        except EOFError:
            print("No input given")

        print("All generations have been processed.")
        print(f"Total generations: {gen_count}")
        print(f"Best chromosome: {[e for e in self.popclass.population[0].value]} {self.popclass.best_fitness}", end="\n")
        suma = 0
        for item in self.popclass.population[0].value:
            x = self.problem.foodlist[item]
            print(x.name, x.calories, x.protein)
            suma += int(x.calories)
        print(f"CALORIAS FINAIS: {suma}\n")
        
        return self.popclass.population[0].value, self.best_fit_values, self.best_calories_gen, self.best_macros_gen 

if __name__ == '__main__':
    data = NutritionDataFrame()

    ga = GeneticAlgorithmOptimization(
        population_length=100, 
        max_iterations=200,
        convergence_rate=0.8,
        elite_size=2,
        mutation_rate=0.03,
        max_portions=5,
        solution_max_size=25,
        solution_min_size=5,
        problem=data,
    )
    
    res, best_fit_values, best_calories_gen, best_macros_gen = ga.run()

    plt.figure(figsize=(18, 6))

    # Plot for macros convergence
    plt.subplot(1, 3, 1)
    # Extracting each macro component
    proteins = [item[0] for item in best_macros_gen]
    carbs = [item[1] for item in best_macros_gen]
    fats = [item[2] for item in best_macros_gen]

    plt.plot(proteins, marker='o', color='blue', label='Proteins')
    plt.plot(carbs, marker='o', color='skyblue', label='Carbs')
    plt.plot(fats, marker='o', color='navy', label='Fats')
    plt.title("Convergence of GA Macros")
    plt.xlabel("Iteration")
    plt.ylabel("Best Macros Sum")
    plt.legend()

    # Plot for fit convergence
    plt.subplot(1, 3, 2)
    plt.plot(best_calories_gen, marker='o', color='green')
    plt.title("Convergence of GA Calories")
    plt.xlabel("Iteration")
    plt.ylabel("Best Calories Sum") 
    
    # Plot for fit convergence
    plt.subplot(1, 3, 3)
    plt.plot(best_fit_values, marker='o', color='red')
    plt.title("Convergence of GA Fit")
    plt.xlabel("Iteration")
    plt.ylabel("Best Fit Sum") 


    plt.tight_layout()
    plt.show()