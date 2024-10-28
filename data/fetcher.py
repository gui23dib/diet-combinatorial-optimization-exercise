import csv
from classes.nutrition import Nutrition

def load_nutrition_data(file_path):
    nutrition_data = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            entry = Nutrition(
                id=row['id'],
                name=row['name'],
                calories=row['calories'],
                fat=row.get('fat', row['total_fat']), 
                protein=row['protein'],
                carbohydrate=row['carbohydrate']
            )
            nutrition_data.append(entry)

    return nutrition_data