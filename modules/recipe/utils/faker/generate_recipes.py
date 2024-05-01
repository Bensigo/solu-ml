import pandas as pd
from faker import Faker
import random

fake = Faker()

common_ingredients = [
    "chicken", "beef", "salmon", "tofu", "rice", 
    "quinoa", "spinach", "broccoli", "apple", 
    "banana", "almond", "oatmeal", "egg", "milk", 
    "cheese", "yogurt", "bell pepper", "carrot", 
    "tomato", "garlic", "onion"
]


food_allergens = ["dairy", "eggs", "fish", "crustacean shellfish", "tree nuts", "peanuts", "wheat", "soybeans", "sesame seeds"]
meal_pref = ["low cabs","keto", "gluten_free", "dairy_free",
    "low_carb", "low_fat", "low_sugar", "high_protein",]


def generate_recipe(num_recipes=100):
    recipes_data = []
    for i in range(num_recipes):
        ingredients = random.sample(common_ingredients, k=random.randint(3, 7))  # choosing 3-7 ingredients
        allergies = random.sample(food_allergens, k=random.randint(0, 2))  # choosing 0-2 allergens
        
        # Remove ingredients that are also allergens
        for allergen in allergies:
            if allergen in ingredients:
                ingredients.remove(allergen)
        
        recipe = {
            "id": i + 1,
            "name": fake.text(max_nb_chars=150),
            "calories": random.randint(100, 800),
            "description": fake.text(max_nb_chars=150),
            "diet_preference": random.choice(["omnivore", "vegan", "vegetarian", "pescetarian", "paleo"]),
            "meal_preference": ', '.join( random.sample(meal_pref, k=random.randint(1, 3)) ),
            "mealType": random.choice(["Breakfast", "Lunch", "Dinner", "Snack"]),
            "duration": random.randint(10, 60),  # Duration in minutes
            "ingredients": ', '.join(ingredients),
            "steps": ' | '.join([fake.sentence() for _ in range(5)]),
            "protein": random.randint(10, 50),
            "fat": random.randint(5, 30),
            "carbs": random.randint(10, 60),
            "allergens": ', '.join(allergies)
        }
        recipes_data.append(recipe)
    return pd.DataFrame(recipes_data)



# Generate and save recipes to CSV
recipes_df = generate_recipe(100)
recipes_df.to_csv('recipes.csv', index=False)

print("Recipes are generated and saved in recipes.csv.")