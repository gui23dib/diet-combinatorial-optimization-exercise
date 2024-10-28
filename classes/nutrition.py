import re

class Nutrition:
    def __init__(self, id, name, calories, fat, protein, carbohydrate):
        self.id = int(id)
        self.name = name
        self.calories = float(calories)
        self.fat = self._to_float(fat)
        self.protein = self._to_float(protein)
        self.carbohydrate = self._to_float(carbohydrate)
        self.macro_fit = 0.0

    def _to_float(self, value):
        numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
        return float(numeric_value[0]) if numeric_value else 0.0

    def __repr__(self):
        return (f"Nutrition(id={self.id}, name='{self.name}', calories={self.calories}, "
                f"macro_fit={self.macro_fit}, fat={self.fat}, protein={self.protein}, "
                f"carbohydrate={self.carbohydrate})")