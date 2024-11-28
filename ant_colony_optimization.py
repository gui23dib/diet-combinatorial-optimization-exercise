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
        self.best_macro_values = []
        
    def _construct_solution(self):
        visited = set()
        visit_counts = {}
        solution = []
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        total_calories = 0
        
        while len(solution) < self.solution_max_size:
            target_protein: float = self.problem.target_protein
            target_fat: float = self.problem.target_fat
            target_carbs: float = self.problem.target_carbs
            
            probabilities = np.array([
                (self.pheromones[i] ** self.alpha) * 
                (1 / (abs(self.problem.foodlist[i].protein - target_protein) + 
                    abs(self.problem.foodlist[i].fat - target_fat) + 
                    abs(self.problem.foodlist[i].carbs - target_carbs) + 1)) ** self.beta 
                if i not in visited or visit_counts.get(i, 0) < self.max_portions else 0
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
                if visit_counts[next_city] >= self.max_portions:
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

        for i in range(self.num_iterations):
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
            print(f"Generation {i} / Best Value: {self.best_value}")
            self.best_cal_values.append(sum(self.problem.foodlist[city].calories for city in self.best_solution))
            self.best_macro_values.append([
                sum(self.problem.foodlist[city].protein for city in self.best_solution),
                sum(self.problem.foodlist[city].carbs for city in self.best_solution),
                sum(self.problem.foodlist[city].fat for city in self.best_solution)
            ])
        return self.best_solution, self.best_values, self.best_cal_values, self.best_macro_values
        
if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from classes.nutrition_dataframe import NutritionDataFrame

    df = NutritionDataFrame()
    aco = AntColonyOptimization(
        problem=df,
        num_ants=100,
        num_iterations=200,
        evaporation_rate=0.6,
        alpha=0.4,
        beta=0.8,
        # pheromone_initial=1.0,
    )
    best_solution, best_values, best_cal_values, best_macro_values = aco.run()

    # Results
    print("Best Solution:", end=' ')
    for i in best_solution: print(int(i), end='') 
    print()

    for food in (df.foodlist[i] for i in best_solution):
        print(f"\t{food.name}: protein={food.protein}, calories={food.calories}")
    print("Total Calories Cost:", sum(df.foodlist[food].calories for food in best_solution))

    plt.figure(figsize=(18, 6))

    # Plot for protein convergence
    plt.subplot(1, 3, 1)
    
    proteins = [item[0] for item in best_macro_values]
    carbs = [item[1] for item in best_macro_values]
    fats = [item[2] for item in best_macro_values]

    plt.plot(proteins, marker='o', color='blue', label='Proteins')
    plt.plot(carbs, marker='o', color='skyblue', label='Carbs')
    plt.plot(fats, marker='o', color='navy', label='Fats')
    plt.title("Convergence of ACO Macros")
    plt.xlabel("Iteration")
    plt.ylabel("Best Macros Sum")
    plt.legend()


    # Plot for fat convergence
    plt.subplot(1, 3, 2)
    plt.plot(best_cal_values, marker='o', color='green')
    plt.title("Convergence of ACO calories")
    plt.xlabel("Iteration")
    plt.ylabel("Best Calories Sum")

    # Plot for pheromone levels
    plt.subplot(1, 3, 3)
    plt.bar(range(len(df.foodlist)), aco.pheromones, color='red', alpha=0.7)
    plt.title("Pheromone Levels for Nodes")
    plt.xlabel("FoodNode")
    plt.ylabel("Pheromone Strength")
    plt.xticks(range(len(df.foodlist)), [f"{i.name}" for i in df.foodlist], rotation=90)

    plt.tight_layout()
    plt.show()