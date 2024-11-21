import matplotlib.pyplot as plt

from ant_colony.ant_colony_optimization import AntColonyOptimization
from ant_colony.nutrition_dataframe import NutritionDataFrame

if __name__ == "__main__":
    df = NutritionDataFrame()
    aco = AntColonyOptimization(
        problem=df,
        num_ants=100,
        num_iterations=500,
        evaporation_rate=0.6,
        alpha=0.4,
        beta=0.8,
        # pheromone_initial=1.0,
    )
    best_solution, best_value, best_values, best_cal_values = aco.run()

    # Results
    print("Best Solution:", end=' ')
    for i in best_solution: print(int(i), end='') 
    print()

    for food in (df.foodlist[i] for i in best_solution):
        print(f"\t{food.name}: protein={food.protein}, calories={food.calories}")
    print("Total Protein Consumption:", best_value)
    print("Total Calories Cost:", sum(df.foodlist[food].calories for food in best_solution))

    plt.figure(figsize=(18, 5))

    plt.subplot(1, 3, 1)
    plt.plot(best_values, marker='o', color='green')
    plt.title("Convergence of ACO protein")
    plt.xlabel("Iteration")
    plt.ylabel("Best protein sum")
    
    plt.subplot(1, 3, 2)
    plt.plot(best_cal_values, marker='o', color='blue')
    plt.title("Convergence of ACO calories")
    plt.xlabel("Iteration")
    plt.ylabel("Best calories sum")

    plt.subplot(1, 3, 3)
    plt.bar(range(len(df.foodlist)), aco.pheromones, color='green', alpha=0.7)
    plt.title("Pheromone Levels for Cities")
    plt.xlabel("FoodNode")
    plt.ylabel("Pheromone Strength")
    plt.xticks(range(len(df.foodlist)), [f"{i.name}" for i in df.foodlist], rotation=90)

    plt.tight_layout()
    plt.show()
