from ant_colony.food import FoodNode


class NutritionDataFrame:
    def __init__(self, foodlist = [], target_macro = 100, max_calories = 2000):
        print("Initializing NutritionDataFrame")
        print("target_macro:", target_macro, type(target_macro))
        print("max_calories:", max_calories, type(max_calories))
        self.foodlist: list[FoodNode] = [
            FoodNode(name="Frango Grelhado", protein=31, calories=165),
            FoodNode(name="Salada de Folhas Verdes", protein=2, calories=15),
            FoodNode(name="Abacate", protein=2, calories=160),
            FoodNode(name="Salmão Grelhado", protein=20, calories=208),
            FoodNode(name="Quinoa Cozida", protein=4, calories=120),
            FoodNode(name="Ovo Cozido", protein=6, calories=70),
            FoodNode(name="Iogurte Grego Natural Sem Açúcar", protein=10, calories=59),
            FoodNode(name="Lentilhas Cozidas", protein=9, calories=116),
            FoodNode(name="Brócolis Cozidos", protein=3, calories=35),
            FoodNode(name="Batata-Doce Assada", protein=2, calories=86),
            FoodNode(name="Feijão Preto", protein=8, calories=127),
            FoodNode(name="Arroz Integral", protein=7, calories=111),
            FoodNode(name="Frango Assado", protein=28, calories=230),
            FoodNode(name="Peito de Peru", protein=29, calories=135),
            FoodNode(name="Espinafre Cozido", protein=3, calories=23),
            FoodNode(name="Tomate", protein=1, calories=18),
            FoodNode(name="Pêssego", protein=1, calories=39),
            FoodNode(name="Cenoura Cozida", protein=1, calories=41),
            FoodNode(name="Alface", protein=1, calories=14),
            FoodNode(name="Pão Branco", protein=7, calories=265),
            FoodNode(name="Batata Frita", protein=3, calories=319),
            FoodNode(name="Refrigerante", protein=0, calories=150),
            FoodNode(name="Chocolate", protein=6, calories=500),
            FoodNode(name="Salgadinhos de Pacote", protein=6, calories=530),
            FoodNode(name="Bolo de Chocolate", protein=5, calories=400),
            FoodNode(name="Coxinha", protein=8, calories=250),
            FoodNode(name="Macarrão Instantâneo", protein=7, calories=440),
            FoodNode(name="Pipoca de Micro-ondas", protein=3, calories=500),
            FoodNode(name="Sorvete de Creme", protein=4, calories=207),
        ]
        self.target_macro: int = target_macro
        self.max_calories: int = max_calories

    def evaluate(self, solution):
        total_macro = sum(self.foodlist[node].protein for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0 
        return total_macro