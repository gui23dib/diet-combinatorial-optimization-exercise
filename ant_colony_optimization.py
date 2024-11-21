import numpy as np

class AntColonyOptimization:
    def __init__(self, problem, num_ants, num_iterations, alpha, beta, evaporation_rate, solution_max_size = 15, max_portions = 5):
        self.problem: NutritionDataFrame = problem
        self.num_ants: int = num_ants
        self.num_iterations: int = num_iterations
        self.alpha: float = alpha
        self.beta: float = beta
        self.evaporation_rate: float = evaporation_rate
        self.solution_max_size: float = solution_max_size
        self.max_portions: int = max_portions
        self.pheromones = np.ones(len(problem.foodlist))
        self.best_solution = None
        self.best_value: float = float('-inf')
        self.best_values = []
        self.best_cal_values = []
        
        self.best_values = []
        self.best_cal_values = []
        self.best_protein_values = []
        self.best_fat_values = []
        self.best_carbs_values = []

    def _construct_solution(self):
        visited = set()
        visit_counts = {}
        solution = []
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        total_calories = 0
        
        while len(solution) < self.solution_max_size:
            target_protein: float = 200
            target_fat: float = 100
            target_carbs: float = 300
            
            probabilities = np.array([
                (self.pheromones[i] ** self.alpha) * 
                (1 / (abs(self.problem.foodlist[i].protein - target_protein) + 
                    abs(self.problem.foodlist[i].fat - target_fat) + 
                    abs(self.problem.foodlist[i].carbs - target_carbs) + 1)) ** self.beta 
                if i not in visited or visit_counts.get(i, 0) < 5 else 0
                for i in range(len(self.problem.foodlist))
            ])
            probabilities /= probabilities.sum() if probabilities.sum() > 0 else 1
            next_city = np.random.choice(range(len(self.problem.foodlist)), p=probabilities)
            
            next_protein = total_protein + self.problem.foodlist[next_city].protein
            next_fat = total_fat + self.problem.foodlist[next_city].fat
            next_carbs = total_carbs + self.problem.foodlist[next_city].carbs
            next_calories = total_calories + self.problem.foodlist[next_city].calories
            
            if next_calories <= self.problem.max_calories:
                solution.append(next_city)
                visit_counts[next_city] = visit_counts.get(next_city, 0) + 1
                if visit_counts[next_city] >= 5:
                    visited.add(next_city)
                total_protein = next_protein
                total_fat = next_fat
                total_carbs = next_carbs
                total_calories = next_calories
            else:
                break
        
        return solution

    def _update_pheromones(self, solutions, values):
        self.pheromones *= (1 - self.evaporation_rate)  # Evaporation
        for solution, value in zip(solutions, values):
            for city in solution:
                self.pheromones[city] += value

    def run(self):

        for _ in range(self.num_iterations):
            solutions = []
            values = []
            for _ in range(self.num_ants):
                solution = self._construct_solution()
                value = self.problem.evaluate(solution)
                solutions.append(solution)
                values.append(value)
                if value > self.best_value:
                    self.best_value = value
                    self.best_solution = solution
            self._update_pheromones(solutions, values)
            self.best_values.append(self.best_value)
            self.best_cal_values.append(sum(self.problem.foodlist[city].calories for city in self.best_solution))
            self.best_protein_values.append(sum(self.problem.foodlist[city].protein for city in self.best_solution))
            self.best_fat_values.append(sum(self.problem.foodlist[city].fat for city in self.best_solution))
            self.best_carbs_values.append(sum(self.problem.foodlist[city].carbs for city in self.best_solution))
        return self.best_solution, self.best_value, self.best_values, self.best_cal_values, self.best_protein_values, self.best_fat_values, self.best_carbs_values
        
if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from classes.nutrition_dataframe import NutritionDataFrame

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
    best_solution, best_value, best_values, best_cal_values, best_protein_values, best_fat_values, best_carbs_values = aco.run()

    # Results
    print("Best Solution:", end=' ')
    for i in best_solution: print(int(i), end='') 
    print()

    for food in (df.foodlist[i] for i in best_solution):
        print(f"\t{food.name}: protein={food.protein}, calories={food.calories}")
    print("Total Protein Consumption:", best_value)
    print("Total Calories Cost:", sum(df.foodlist[food].calories for food in best_solution))

    plt.figure(figsize=(18, 6))

    # Plot for protein convergence
    plt.subplot(1, 4, 1)
    plt.plot(best_protein_values, marker='o', color='green')
    plt.title("Convergence of ACO Protein")
    plt.xlabel("Iteration")
    plt.ylabel("Best Protein Sum")

    # Plot for fat convergence
    plt.subplot(1, 4, 2)
    plt.plot(best_fat_values, marker='o', color='red')
    plt.title("Convergence of ACO Fat")
    plt.xlabel("Iteration")
    plt.ylabel("Best Fat Sum")

    # Plot for carbs convergence
    plt.subplot(1, 4, 3)
    plt.plot(best_carbs_values, marker='o', color='orange')
    plt.title("Convergence of ACO Carbs")
    plt.xlabel("Iteration")
    plt.ylabel("Best Carbs Sum")

    # Plot for pheromone levels
    plt.subplot(1, 4, 4)
    plt.bar(range(len(df.foodlist)), aco.pheromones, color='green', alpha=0.7)
    plt.title("Pheromone Levels for Cities")
    plt.xlabel("FoodNode")
    plt.ylabel("Pheromone Strength")
    plt.xticks(range(len(df.foodlist)), [f"{i.name}" for i in df.foodlist], rotation=90)

    plt.tight_layout()
    plt.show()