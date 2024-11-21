import csv

from classes.food import FoodNode

class NutritionDataFrame:
    def __init__(self, foodlist = None, target_macro = 100, max_calories = 2000):
        print("Initializing NutritionDataFrame")
        print("target_macro:", target_macro, type(target_macro))
        print("max_calories:", max_calories, type(max_calories))
        self.foodlist: list[FoodNode] = foodlist or self.get_csv('data/foods.csv')
        self.target_macro: int = target_macro
        self.max_calories: int = max_calories

    def evaluate(self, solution):
        total_macro = sum(self.foodlist[node].protein for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0 
        return total_macro
    
    def get_csv(self, file_path) -> list[FoodNode]:
        objects = []

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')

            for row in reader:
                entry = FoodNode(
                    name=row['Nome'],
                    protein=float(row['Proteína']),
                    calories=float(row['Calorias']),
                    fat=float(row['Gordura']),
                    carbs=float(row['Carboidratos'])
                )
                objects.append(entry)

        return objects

if __name__ == '__main__':
    data = NutritionDataFrame()
    for i in data.foodlist:
        print(i.name, i.protein, i.calories, i.fat, i.carbs)