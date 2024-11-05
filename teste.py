import data.fetcher as fetcher
from classes.nutrition import Nutrition
import heapq



if __name__ == '__main__':
    nodes: list[Nutrition] = fetcher.load_nutrition_data('data/sample_nutrition_data.csv')

    obj_kcal = 1800 #utils.get_user_input()
    refeicoes = [(None, 0.1), (None, 0.6), (None, 0.3)]
    
    print("Preparando dados...")
    
    edges = [(u, v) for u in nodes for v in nodes if u != v]
    
    print("Calculando fitness...")
    
    target_calories = 2000
    target_macros = 1
    weight_calories = 0.7
    weight_macros = 0.3
    
    print("Calculando pesos das arestas...")

    # Dicionário para armazenar as arestas mais próximas para cada nó
    edge_weights = {}

    for u in nodes:
        # Calcula o peso de cada aresta e mantém as 5 melhores
        closest_edges = []
        for v in nodes:
            if u.id != v.id:
                cal_diff = abs((u.calories + v.calories) / 2 - target_calories)
                macro_diff = abs((u.macro_fit + v.macro_fit) / 1)
                weight = weight_calories * cal_diff + weight_macros * macro_diff
                # Mantém as 5 menores distâncias
                if len(closest_edges) < 5:
                    heapq.heappush(closest_edges, (-weight, v.id))  # Negativo para inverter o heap
                else:
                    heapq.heappushpop(closest_edges, (-weight, v.id))

        # Adiciona os 5 mais próximos ao grafo final
        edge_weights[u.id] = [(v_id, -w) for w, v_id in closest_edges]

    # Exibe o grafo simplificado com as conexões mais próximas
    for u_id, connections in edge_weights.items():
        print(f"Alimento {u_id} conectado a: {connections}")