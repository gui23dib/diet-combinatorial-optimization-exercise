class FoodNode:
    def __init__(self, protein, calories, fat, carbs, name):
        self.protein: int = protein
        self.calories: int = calories
        self.carbs: int = carbs
        self.fat: int = fat
        self.name: str = name