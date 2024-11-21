from ant_colony.food import FoodNode


class NutritionDataFrame:
    def __init__(self):
        self.foodlist: list[FoodNode] = [
            FoodNode(name="Feijão com Arroz", protein=20, calories=451),         # Feijão com arroz
            FoodNode(name="Pão Francês com Manteiga", protein=5, calories=253),    # Pão francês com manteiga
            FoodNode(name="Café com Leite", protein=3, calories=154),               # Café com leite
            FoodNode(name="Bife com Batata Frita", protein=25, calories=707),        # Bife com batata frita
            FoodNode(name="Macarrão com Molho de Tomate", protein=15, calories=404), # Macarrão com molho de tomate
            FoodNode(name="Coxinha", protein=6, calories=259),                      # Coxinha
            FoodNode(name="Tapioca", protein=8, calories=206),                      # Tapioca
            FoodNode(name="Pão de Queijo", protein=7, calories=207),                 # Pão de queijo
            FoodNode(name="Sanduíche de Presunto e Queijo", protein=12, calories=305), # Sanduíche de presunto e queijo
            FoodNode(name="Feijoada", protein=25, calories=759),                    # Feijoada
            FoodNode(name="Churrasco com Arroz e Feijão", protein=35, calories=909),  # Churrasco com arroz e feijão
            FoodNode(name="Acarajé", protein=5, calories=307),                       # Acarajé
            FoodNode(name="Empadinha", protein=7, calories=251),                     # Empadinha
            FoodNode(name="Bolinho de Bacalhau", protein=10, calories=303),           # Bolinho de bacalhau
            FoodNode(name="Baião de Dois", protein=20, calories=604),                 # Baião de dois
            FoodNode(name="Moqueca", protein=18, calories=404),                       # Moqueca
            FoodNode(name="Escondidinho de Carne Seca", protein=18, calories=507),     # Escondidinho de carne seca
            FoodNode(name="Farofa", protein=5, calories=201),                         # Farofa
            FoodNode(name="Arroz de Feijão Tropeiro", protein=15, calories=558),        # Arroz de feijão tropeiro
            FoodNode(name="Churrasco com Farofa e Arroz", protein=35, calories=808),    # Churrasco com farofa e arroz
            FoodNode(name="Torta de Frango", protein=12, calories=353),                # Torta de frango
        ]
        self.target_macro: int = 100
        self.max_calories: int = 2000

    def evaluate(self, solution):
        total_macro = sum(self.foodlist[node].protein for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0  # Invalid solution
        return total_macro