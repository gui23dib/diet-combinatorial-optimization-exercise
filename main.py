from data.fetcher import load_nutrition_data
from classes.nutrition import Nutrition
import utils
import genetic_alg


def get_data_overall_fitness(df: list[Nutrition], carb, prot, fat) -> list[Nutrition]:
    for row in df:
        total_macros = row.carbohydrate + row.protein + row.fat
        if(total_macros == 0):
            df.remove(row)
            continue
        
        fit_medio += abs(carb - (row.carbohydrate / total_macros))
        fit_medio  += abs(prot - (row.protein / total_macros))
        fit_medio += abs(fat - (row.fat / total_macros))
        row.macro_fit = 1 / (1 + (fit_medio / 3))
    return df

if __name__ == '__main__':
    data: list[Nutrition] = load_nutrition_data('data/nutrition_withouth_0_calories.csv')

    obj_kcal = utils.get_user_input()
    carb, prot, fat = (0.5, 0.3, 0.2)
    refeicoes = [(None, 0.1), (None, 0.6), (None, 0.3)]
    
    get_data_overall_fitness(data, carb, prot, fat)

    for refeicao, distribuicao in refeicoes:
        #refeicao = genetic_alg(data, (distribuicao * obj_kcal))
        #refeicao = ant_colony(data, (distribuicao * obj_kcal))
        print(refeicao, distribuicao)
