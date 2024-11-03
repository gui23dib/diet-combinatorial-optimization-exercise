from data.fetcher import load_nutrition_data
from classes.nutrition import Nutrition
import utils

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
    nodes: list[Nutrition] = load_nutrition_data('data/nutrition_without_0_calories.csv')

    obj_kcal = utils.get_user_input()
    carb, prot, fat = (0.5, 0.3, 0.2)
    refeicoes = [(None, 0.1), (None, 0.6), (None, 0.3)]
    
    edges = [(u, v) for u in nodes for v in nodes if u != v]

    
    get_data_overall_fitness(nodes, carb, prot, fat)
    target_calories = 2000
    target_macros = 1
    weight_calories = 0.7
    weight_macros = 0.3

    edge_weights = {}
    for u, v in edges:
        # Calculando o peso da aresta com base nas diferenças dos atributos em relação à meta
        cal_diff = abs((u.calories + v.calories) / 2 - target_calories)
        macro_diff = abs((u.macro_fit + v.macro_fit) / 2 - 1.0)
        weight = weight_calories * cal_diff + weight_macros * macro_diff
        edge_weights[(u.id, v.id)] = weight

    # Representação manual do grafo e seus pesos
    graph_representation = ""

    # Exibir nós com seus atributos
    graph_representation += "NÓS (Alimentos):\n"
    for node in nodes:
        graph_representation += f"{node.name} (ID {node.id}): {node.calories} cal, Macro Fit = {node.macro_fit:.2f}\n"

    # Exibir arestas com seus pesos
    graph_representation += "\nARESTAS (Conexões entre alimentos com pesos):\n"
    for edge, weight in edge_weights.items():
        graph_representation += f"Alimento {edge[0]} - Alimento {edge[1]}: Peso = {weight:.2f}\n"

    # Exibir o grafo
    print(graph_representation)