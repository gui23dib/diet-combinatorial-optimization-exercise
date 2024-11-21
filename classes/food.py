class FoodNode:
    def __init__(self, protein, calories, fat, carbs, name):
        self.protein: float = protein
        self.calories: float = calories
        self.carbs: float = carbs
        self.fat: float = fat
        self.name: str = name