import re

def get_datapoint_overall_fitness(data, carb, prot, fat):
    total_macros = data.carbohydrate + data.protein + data.fat
    if(total_macros == 0): return data

    fit_medio = abs(self.carb - (data.carbohydrate / total_macros))
    fit_medio  += abs(self.prot - (data.protein / total_macros))
    fit_medio += abs(self.fat - (data.fat / total_macros))
    data.macro_fit = 1 / (1 + (fit_medio / 3))
    return data

class Nutrition():
    def __init__(self, propid, name, calories, fat, protein, carbohydrate):
        self.id = int(propid)
        self.name = name
        self.calories = float(calories)

        self.fat = self._to_float(fat)
        self.protein = self._to_float(protein)
        self.carb = self._to_float(carbohydrate)

    def _to_float(self, value):
        numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
        return float(numeric_value[0]) if numeric_value else 0.0

    def __repr__(self):
        return (f"Nutrition(id={self.id}, name='{self.name}', calories={self.calories}, "
                f"macro_fit={self.macro_fit}")