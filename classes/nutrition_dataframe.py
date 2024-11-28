import csv

from classes.food import FoodNode

def get_csv(file_path) -> list[FoodNode]:
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

class NutritionDataFrame:
    def __init__(
        self, 
        foodlist: list[FoodNode] = None, 
        max_calories = 2000, 
        target_protein = 200, 
        target_carbs = 100, 
        target_fat = 50, 
        calories_weight = 0.5,
        macro_weight = 0.5
    ):
        print("Initializing NutritionDataFrame")
        print("max_calories:", max_calories, type(max_calories))
        self.foodlist: list[FoodNode] = foodlist or get_csv('data/foods.csv')
        
        self.target_protein: int = target_protein
        self.target_fat: int = target_fat
        self.target_carbs: int = target_carbs
        print("target_protein:", target_protein)
        print("target_fat:", target_fat)
        print("target_carbs:", target_carbs)
        
        self.max_calories: int = max_calories
        self.calories_weight: float = calories_weight
        self.macros_weight: float = macro_weight

    def evaluate(self, solution):
        total_protein = sum(self.foodlist[node].protein for node in solution)
        total_fat = sum(self.foodlist[node].fat for node in solution)
        total_carbs = sum(self.foodlist[node].carbs for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0
        
        protein_score = max(0, self.target_protein - abs(self.target_protein - total_protein))
        fat_score = max(0, self.target_fat - abs(self.target_fat - total_fat))
        carbs_score = max(0, self.target_carbs - abs(self.target_carbs - total_carbs))
        
        calorie_score = max(0, self.max_calories - abs(self.max_calories - total_calorie_cost))
        
        return ((protein_score + fat_score + carbs_score) * self.macros_weight) + (calorie_score * self.calories_weight )

if __name__ == '__main__':
    data = NutritionDataFrame()
    for i in data.foodlist:
        print(i.name, i.protein, i.calories, i.fat, i.carbs)