import json

with open('ingredients.json') as f:
    ingredients = json.load(f)

i = 0
for category in ingredients:
    i += len(ingredients[category])
    #print(category, ingredients[category])

ingredient = input(f'Search for an ingredient from {i} ingredients: ')
print(f'{ingredient} could be {[i for c, v in ingredients.items() for i in v if ingredient.strip().lower() in i.lower()]}')

