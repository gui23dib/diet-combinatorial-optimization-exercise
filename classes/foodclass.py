class Nutrition:
    def __init__(self, energy, protein, fat, saturated_fat, carbohydrate, sugars, dietary_fiber, sodium):
        self.energy = energy  # in kcal
        self.protein = protein  # in grams
        self.fat = fat  # in grams
        self.saturated_fat = saturated_fat  # in grams
        self.carbohydrate = carbohydrate  # in grams
        self.sugars = sugars  # in grams
        self.dietary_fiber = dietary_fiber  # in grams
        self.sodium = sodium  # in mg

    def __str__(self):
        return (f"Nutrition(energy={self.energy}, protein={self.protein}, fat={self.fat}, "
                f"saturated_fat={self.saturated_fat}, carbohydrate={self.carbohydrate}, "
                f"sugars={self.sugars}, dietary_fiber={self.dietary_fiber}, sodium={self.sodium})")


class FoodItem:
    def __init__(self, id, name, nutrition, tags = None, contains = None):
        self.id = id
        self.name = name
        self.nutrition = nutrition
        self.tags = tags
        self.contains = contains

    def __str__(self):
        return f"FoodItem(id={self.id} name={self.name} nutrition={self.nutrition} tags={self.tags})"
