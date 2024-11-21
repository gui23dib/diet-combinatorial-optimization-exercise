from classes.food import FoodNode
from classes.nutrition_dataframe import NutritionDataFrame
from data.tools.utils import print_stats
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
            solution_size: int = 10,
            population_length: int = 100,
        ):
        self.problem = problem
        self.popclass: PopulationClass = PopulationClass()
        self.popclass.populate(solution_size, population_length, len(problem.foodlist) - 1)
        
        #self.popclass.population: list[ChromosomeClass] = self.popclass.population
        
        self.solution_size = solution_size
        self.popclass.population_length = population_length
        self.mutation_rate = mutation_rate
        self.max_iterations: int = max_iterations

        self.best_fit_values: list = [] #melhores fit por geração
        self.best_calories_gen: list = [] #melhores calorias por geração
        self.best_proteins_gen: list = [] #melhores proteínas por geração
        
    #Calcula fitness
    def fitness(self) -> list[ChromosomeClass]:
        for chromossome in self.popclass.population:
            total_protein = 0
            total_carbs = 0
            total_fats = 0
            total_calories = 0
            gene_count = {}
            
            for _, gene in enumerate(chromossome.value):
                if gene not in gene_count:
                    gene_count[gene] = 0
                gene_count[gene] += 1
                
                if gene_count[gene] > 3:
                    chromossome.fitness = 0
                    break
                total_calories += int(self.problem.foodlist[gene].calories)
                total_protein += int(self.problem.foodlist[gene].protein)
                total_carbs += int(self.problem.foodlist[gene].carbs)
                total_fats += int(self.problem.foodlist[gene].fat)
            else:
                if total_calories > self.problem.max_calories:
                    chromossome.fitness = 0
                else:
                    protein_diff = abs(self.problem.target_protein - total_protein)
                    carbs_diff = abs(self.problem.target_carbs - total_carbs)
                    fats_diff = abs(self.problem.target_fat - total_fats)
                    chromossome.fitness = 1 / (1 + protein_diff + carbs_diff + fats_diff)  # Higher fitness for smaller differences
        return self.popclass.population


    #Roleta Viciada
    def mating_pool_roulette(self):
        total_net_fitness = sum([chromosome.fitness for chromosome in self.popclass.population])
        result = random.choices(self.popclass.population, weights=[chromosome.fitness / total_net_fitness for chromosome in self.popclass.population], k=2)

        pointer: int = random.randint(1, len(result[0].value) - 1)
        result[0] = result[0].reproduce(result[1], pointer)
        result[1] = result[1].reproduce(result[0], pointer)

        return result

    #Cria uma nova geração ordenada
    def new_generation(self, n_survivors: int = 2) -> list[ChromosomeClass]:
        return sorted(self.popclass.population, key=lambda x: x.fitness, reverse=True)[:n_survivors]

    def run(self) -> int:
        try:
            gen_count: int = 0
            
            while self.popclass.best_fitness != 1.0 and gen_count <= self.max_iterations:
                self.popclass.population = self.fitness()
                self.popclass.sort_population() # sort population by fitness (already defines the best fitness)
                self.best_fit_values.append(self.popclass.best_fitness) 
                soma_calorias = 0
                soma_proteinas = 0
                for food in self.popclass.population[0].value:
                    soma_calorias += self.problem.foodlist[food].calories
                    soma_proteinas += self.problem.foodlist[food].protein
                self.best_calories_gen.append(soma_calorias)
                self.best_proteins_gen.append(soma_proteinas)

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
        
        return self.popclass.population[0].value, self.best_fit_values, self.best_calories_gen, self.best_proteins_gen 

if __name__ == '__main__':
    data = NutritionDataFrame()

    ga = GeneticAlgorithmOptimization(
        solution_size=10, 
        population_length=100, 
        problem=data,
    )
    
    res, best_fit_values, best_calories_gen, best_proteins_gen = ga.run()

    plt.figure(figsize=(18, 6))

    # Plot for fit convergence
    plt.subplot(1, 4, 1)
    plt.plot(best_fit_values, marker='o', color='green')
    plt.title("Convergence of GA Fit")
    plt.xlabel("Iteration")
    plt.ylabel("Best Fit Sum") 

    # Plot for fit convergence
    plt.subplot(1, 4, 2)
    plt.plot(best_calories_gen, marker='o', color='green')
    plt.title("Convergence of GA Calories")
    plt.xlabel("Iteration")
    plt.ylabel("Best Calories Sum") 

    # Plot for fit convergence
    plt.subplot(1, 4, 2)
    plt.plot(best_proteins_gen, marker='o', color='green')
    plt.title("Convergence of GA Proteins")
    plt.xlabel("Iteration")
    plt.ylabel("Best Proteins Sum")

    plt.tight_layout()
    plt.show()

