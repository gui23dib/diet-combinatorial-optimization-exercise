import json
from classes.foodclass import FoodItem

def fetch_food_data(isprint = False):
    with open('./food.json', 'r', encoding="utf-8") as file:
        data_dict = json.load(file)

    data = []
    for food in data_dict:
        data.append(FoodItem(**food))

    print("Data fetched successfully!")
    if isprint:
        print(len(data), "items fetched.")
        for e in data:
            print(e)

    return data
