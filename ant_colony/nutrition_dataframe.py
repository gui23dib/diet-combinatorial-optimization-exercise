from ant_colony.food import FoodNode


class NutritionDataFrame:
    def __init__(self, foodlist = [], target_macro = 100, max_calories = 2000):
        self.foodlist: list[FoodNode] = [
            FoodNode(name="Feijão com Arroz", protein=20, calories=451),
            FoodNode(name="Pão Francês com Manteiga", protein=5, calories=253),
            FoodNode(name="Café com Leite", protein=3, calories=154),
            FoodNode(name="Bife com Batata Frita", protein=25, calories=707),
            FoodNode(name="Macarrão com Molho de Tomate", protein=15, calories=404),
            FoodNode(name="Coxinha", protein=6, calories=259),
            FoodNode(name="Tapioca", protein=8, calories=206),
            FoodNode(name="Pão de Queijo", protein=7, calories=207),
            FoodNode(name="Sanduíche de Presunto e Queijo", protein=12, calories=305),
            FoodNode(name="Feijoada", protein=25, calories=759),
            FoodNode(name="Churrasco com Arroz e Feijão", protein=35, calories=909),
            FoodNode(name="Acarajé", protein=5, calories=307),
            FoodNode(name="Empadinha", protein=7, calories=251),
            FoodNode(name="Bolinho de Bacalhau", protein=10, calories=303),
            FoodNode(name="Baião de Dois", protein=20, calories=604),
            FoodNode(name="Moqueca", protein=18, calories=404),
            FoodNode(name="Escondidinho de Carne Seca", protein=18, calories=507),
            FoodNode(name="Farofa", protein=5, calories=201),
            FoodNode(name="Arroz de Feijão Tropeiro", protein=15, calories=558),
            FoodNode(name="Churrasco com Farofa e Arroz", protein=35, calories=808),
            FoodNode(name="Torta de Frango", protein=12, calories=353),
        ]
        self.target_macro: int = target_macro
        self.max_calories: int = max_calories

    def evaluate(self, solution):
        total_macro = sum(self.foodlist[node].protein for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0  # Invalid solution
        return total_macro