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
            dataframe: list[FoodNode],
            objective: tuple[int, int],
            mutation_rate: float = 0.05,
            max_iterations: int = 500,
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

        self.best_fit_values: list = [] #melhores fit por geração
        self.best_calories_gen: list = [] #melhores calorias por geração
        self.best_proteins_gen: list = [] #melhores proteínas por geração
        
    #Calcula fitness
    def fitness(self, obj: tuple[int, int]) -> list[ChromosomeClass]:
        for chromossome in self.population:
            points = 0
            diff_cal = 0
            for _, gene in enumerate(chromossome.value):
                diff_cal += int(self.dataframe[gene].calories)
            
            points = abs(obj[0] - diff_cal)

            chromossome.fitness = 1 / (1 + points) 
        return self.population

    #Roleta Viciada
    def mating_pool_roulette(self):
        total_net_fitness = sum([chromosome.fitness for chromosome in self.population])
        result = random.choices(self.population, weights=[chromosome.fitness / total_net_fitness for chromosome in self.population], k=2)

        pointer: int = random.randint(1, len(result[0].value) - 1)
        result[0] = result[0].reproduce(result[1], pointer)
        result[1] = result[1].reproduce(result[0], pointer)

        return result

    #Cria uma nova geração ordenada
    def new_generation(self, n_survivors: int = 2) -> list[ChromosomeClass]:
        return sorted(self.population, key=lambda x: x.fitness, reverse=True)[:n_survivors]

    def run(self) -> int:
        try:
            gen_count: int = 0

            population: PopulationClass = PopulationClass()#Instancia pop
            population.populate(self.solution_size, self.population_length, len(self.dataframe) - 1)#Inicia pop

            while population.best_fitness != 1.0 and gen_count <= self.max_iterations:
                population.population = self.fitness(self.objective)
                population.sort_population() # sort population by fitness (already defines the best fitness)
                self.best_fit_values.append(population.best_fitness) 
                soma_calorias = 0
                soma_proteinas = 0
                for food in population.population[0].value:
                    soma_calorias += self.dataframe[food].calories
                    soma_proteinas += self.dataframe[food].protein
                self.best_calories_gen.append(soma_calorias)
                self.best_proteins_gen.append(soma_proteinas)

                print_stats(population, gen_count)

                new_population: list[ChromosomeClass] = self.new_generation()
                while len(new_population) < len(population.population):
                    for child in self.mating_pool_roulette(): # pick your mating pool method here
                        new_population.append(ChromosomeClass(child.mutate(self.mutation_rate, len(self.dataframe) - 1)))

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
            x = self.dataframe[item]
            print(x.name, x.calories, x.protein)
            suma += int(x.calories)
        print(f"CALORIAS FINAIS: {suma}\n")
        
        return population.population[0].value, self.best_fit_values, self.best_calories_gen, self.best_proteins_gen 

if __name__ == '__main__':
    data = NutritionDataFrame()

    ga = GeneticAlgorithmOptimization(
        solution_size=10, 
        population_length=100, 
        dataframe=data.foodlist,
        objective=(2000, 200)
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

