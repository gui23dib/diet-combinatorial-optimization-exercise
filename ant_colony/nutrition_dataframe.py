from ant_colony.food import FoodNode


class NutritionDataFrame:
    def __init__(self, foodlist = [], target_macro = 100, max_calories = 2000):
        print("Initializing NutritionDataFrame")
        print("target_macro:", target_macro, type(target_macro))
        print("max_calories:", max_calories, type(max_calories))
        self.foodlist: list[FoodNode] = [
            FoodNode(name="Frango Grelhado", protein=31, calories=165, fat=4, carbs=0),
FoodNode(name="Salada de Folhas Verdes", protein=2, calories=15, fat=0, carbs=3),
FoodNode(name="Abacate", protein=2, calories=160, fat=15, carbs=9),
FoodNode(name="Salmão Grelhado", protein=20, calories=208, fat=12, carbs=0),
FoodNode(name="Quinoa Cozida", protein=4, calories=120, fat=2, carbs=21),
FoodNode(name="Ovo Cozido", protein=6, calories=70, fat=5, carbs=1),
FoodNode(name="Iogurte Grego Natural Sem Açúcar", protein=10, calories=59, fat=0, carbs=4),
FoodNode(name="Lentilhas Cozidas", protein=9, calories=116, fat=0, carbs=20),
FoodNode(name="Brócolis Cozidos", protein=3, calories=35, fat=0, carbs=7),
FoodNode(name="Batata-Doce Assada", protein=2, calories=86, fat=0, carbs=20),
FoodNode(name="Feijão Preto", protein=8, calories=127, fat=1, carbs=23),
FoodNode(name="Arroz Integral", protein=7, calories=111, fat=1, carbs=23),
FoodNode(name="Frango Assado", protein=28, calories=230, fat=9, carbs=0),
FoodNode(name="Peito de Peru", protein=29, calories=135, fat=1, carbs=0),
FoodNode(name="Espinafre Cozido", protein=3, calories=23, fat=0, carbs=4),
FoodNode(name="Tomate", protein=1, calories=18, fat=0, carbs=4),
FoodNode(name="Pêssego", protein=1, calories=39, fat=0, carbs=10),
FoodNode(name="Cenoura Cozida", protein=1, calories=41, fat=0, carbs=10),
FoodNode(name="Alface", protein=1, calories=14, fat=0, carbs=3),
FoodNode(name="Pão Branco", protein=7, calories=265, fat=3, carbs=49),
FoodNode(name="Batata Frita", protein=3, calories=319, fat=17, carbs=41),
FoodNode(name="Refrigerante", protein=0, calories=150, fat=0, carbs=39),
FoodNode(name="Chocolate", protein=6, calories=500, fat=30, carbs=60),
FoodNode(name="Salgadinhos de Pacote", protein=6, calories=530, fat=30, carbs=50),
FoodNode(name="Bolo de Chocolate", protein=5, calories=400, fat=20, carbs=45),
FoodNode(name="Coxinha", protein=8, calories=250, fat=15, carbs=20),
FoodNode(name="Macarrão Instantâneo", protein=7, calories=440, fat=20, carbs=60),
FoodNode(name="Pipoca de Micro-ondas", protein=3, calories=500, fat=27, carbs=60),
FoodNode(name="Sorvete de Creme", protein=4, calories=207, fat=11, carbs=24),
        ]
        self.target_macro: int = target_macro
        self.max_calories: int = max_calories

    def evaluate(self, solution):
        total_macro = sum(self.foodlist[node].protein for node in solution)
        total_calorie_cost = sum(self.foodlist[node].calories for node in solution)
        
        if total_calorie_cost > self.max_calories:
            return 0 
        return total_macro