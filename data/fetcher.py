import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
from classes.nutrition import Nutrition

def load_nutrition_data(file_path) -> list[Nutrition]:
    nutrition_data = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            entry = Nutrition(
                propid=row['id'],
                name=row['name'],
                calories=row['calories'],
                fat=row.get('fat', row['total_fat']), 
                protein=row['protein'],
                carbohydrate=row['carbohydrate']
            )
            nutrition_data.append(entry)

    return nutrition_data

if __name__ == '__main__':
    data = load_nutrition_data('data/nutrition_without_0_calories.csv')
    for d in data:
        print(d)
