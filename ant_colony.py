
from classes.nutrition import Nutrition
from data.fetcher import load_nutrition_data
from classes.ant import AntClass
from classes.ant_population import AntPopulation

if __name__ == '__main__':
    data: list[Nutrition] = load_nutrition_data('data/sample_nutrition_data.csv') #criando a lista do arquivo csv

    population: AntPopulation = AntPopulation()

    population.populate()

        
    
    