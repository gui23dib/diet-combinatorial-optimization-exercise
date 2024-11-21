from classes.population import PopulationClass
from classes.chromossome import ChromosomeClass
from Tools.utils import print_stats
import random
from data.fetcher import load_nutrition_data
from classes.nutrition import Nutrition
import Tools.utils as utils
import genetic_alg
import os

def fitness(population: list[ChromosomeClass], obj: (int, int), df: list[Nutrition]) -> list[ChromosomeClass]:
    for chromossome in population:
        points = 0
        diff_cal = 0
        for i, gene in enumerate(chromossome.value):
            diff_cal += df[gene].calories
        
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

def gen_alg(objective: (int, int), dataframe: list[Nutrition]):
    if True:
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
        sumb = 0
        for item in population.population[0].value:
            x = data[item]
            print(x.name, x.calories, x.macro_fit)
            suma += x.calories
            sumb += x.macro_fit
        print(f"CALORIAS FINAIS: {suma}\nMACRO FIT FINAL: {sumb / 10}")

if __name__ == '__main__':
    data: list[Nutrition] = load_nutrition_data('data/alimentos_nutricionais_10.csv')

    obj_kcal = 2000 #utils.get_user_input()

    gen_alg(objective=(obj_kcal,1.0), dataframe=data)
# #---------------------------------------------------------------------------------
# from classes.population import PopulationClass
# from classes.chromossome import ChromosomeClass
# from utils import print_stats
# import random
# from data.fetcher import load_nutrition_data
# from classes.nutrition import Nutrition
# import utils
# import genetic_alg
# import os


# def fitness(population: list[ChromosomeClass], obj: (int, int), df: list[Nutrition]) -> list[ChromosomeClass]:
#     """
#     Avalia o fitness de cada cromossomo na população com base em dois objetivos: calorias e proteínas.
#     Também evita que um único alimento seja desproporcionalmente mais importante que os outros ("super alimento").
    
#     :param population: Lista de cromossomos a serem avaliados
#     :param obj: Tuple com o objetivo de calorias e proteínas (kcal, proteínas)
#     :param df: Lista de dados nutricionais contendo calorias e proteínas
#     :return: População com fitness atualizado
#     """
#     for chromossome in population:
#         # Variáveis para acumular as diferenças de calorias e proteínas
#         diff_cal = 0
#         diff_macro_fit = 0

#         # Avaliamos cada gene (alimento) no cromossomo
#         for i, gene in enumerate(chromossome.value):
#             diff_cal += df[gene].calories
#             diff_macro_fit += df[gene].macro_fit  # Considerando também a proteína

#         # Calcula a diferença entre o objetivo e o valor atual de calorias e proteínas
#         diff_cal_points = abs(obj[0] - diff_cal) * 0.8
#         diff_macro_fit_points = abs(obj[1] - diff_macro_fit) * 0.2

#         # Fitness agora leva em conta tanto calorias quanto proteínas
#         total_diff = diff_cal_points + diff_macro_fit_points

#         # Define o fitness como inversamente proporcional à soma das diferenças (quanto menor, melhor)
#         chromossome.fitness = 1 / (1 + total_diff)

#     return population


# def mating_pool_roulette(population: list[ChromosomeClass]):
#     """
#     Seleciona dois cromossomos para reprodução utilizando roleta de probabilidades proporcionais ao fitness.
    
#     :param population: Lista de cromossomos a serem selecionados
#     :return: Dois novos cromossomos filhos
#     """
#     total_net_fitness = sum([chromosome.fitness for chromosome in population])
#     result = random.choices(population, weights=[chromosome.fitness / total_net_fitness for chromosome in population], k=2)

#     pointer: int = random.randint(1, len(result[0].value) - 1)

#     # Reprodução por cruzamento (crossover)
#     result[0] = result[0].reproduce(result[1], pointer)
#     result[1] = result[1].reproduce(result[0], pointer)

#     return result


# def new_generation(population: list[ChromosomeClass], n_survivors: int = 2) -> list[ChromosomeClass]:
#     """
#     Gera a nova geração mantendo os n melhores indivíduos da geração anterior.
    
#     :param population: Lista de cromossomos da geração atual
#     :param n_survivors: Número de indivíduos que sobrevivem diretamente (elitismo)
#     :return: Nova geração
#     """
#     return sorted(population, key=lambda x: x.fitness, reverse=True)[:n_survivors]


# def gen_alg(objective: (int, int), dataframe: list[Nutrition]):
#     """
#     Executa o algoritmo genético para encontrar uma solução que se aproxima do objetivo de calorias e proteínas.
    
#     :param objective: Tuple com o objetivo de calorias e proteínas
#     :param dataframe: Lista de dados nutricionais
#     """
#     try:
#         max_iterations: int = 10000
#         solution_size = 10
#         population_length = 100
#         mutation_rate = 0.05

#         gen_count: int = 0

#         # Inicializa a população
#         population: PopulationClass = PopulationClass()
#         population.populate(solution_size, population_length, len(dataframe) - 1)

#         # Loop até atingir o máximo de iterações ou encontrar a melhor solução
#         while population.best_fitness != 1.0 and gen_count <= max_iterations:
#             population.population = fitness(population.population, objective, dataframe)
#             population.sort_population()  # Ordena a população com base no fitness

#             print_stats(population, gen_count)

#             # Gera nova população a partir dos sobreviventes
#             new_population: list[ChromosomeClass] = new_generation(population.population)
#             while len(new_population) < len(population.population):
#                 for child in mating_pool_roulette(population.population):  # Método de reprodução escolhido
#                     new_population.append(ChromosomeClass(child.mutate(mutation_rate, len(dataframe) - 1)))

#             population.population = new_population
#             gen_count += 1

#     except KeyboardInterrupt:
#         print("Process interrupted by user")
#     except EOFError:
#         print("No input given")

#     print("All generations have been processed.")
#     print(f"Total generations: {gen_count}")
#     print(f"Best chromosome: {[e for e in population.population[0].value]} {population.best_fitness}", end="\n")

#     # Exibir o cromossomo final
#     total_calories = 0
#     total_macro_fit = 0
#     for item in population.population[0].value:
#         nutrient = dataframe[item]
#         print(nutrient.name, nutrient.calories, nutrient.macro_fit)
#         total_calories += nutrient.calories
#         total_macro_fit += nutrient.macro_fit 

#     # Resultado final
#     print(f"CALORIAS FINAIS: {total_calories}\nPROTEÍNAS FINAIS: {total_macro_fit / 10}")


# if __name__ == '__main__':
#     # Carrega os dados nutricionais
#     data: list[Nutrition] = load_nutrition_data('data/alimentos_nutricionais_10.csv')

#     obj_kcal = 2000  # Objetivo de calorias do usuário
#     obj_prot = 300  # Objetivo de proteínas do usuário

#     # Inicia o algoritmo genético com objetivos de calorias e proteínas
#     gen_alg(objective=(obj_kcal, obj_prot), dataframe=data)
