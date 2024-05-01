import pandas as pd
from faker import Faker
import random

fake = Faker()

food_allergens = ["dairy", "eggs", "fish", "crustacean shellfish", "tree nuts", "peanuts", "wheat", "soybeans", "sesame seeds"]


def generate_user_profile(num_profiles=100):
    user_profiles_data = []
    for index in range(num_profiles):
        # Generate total energy expenditure (TDEE) based on a normal distribution around 2000 kcal/day
        tdee = max(1200, min(2800, int(random.gauss(2000, 300))))
        
        # Calculate macronutrient distribution based on typical percentages
        protein_percent = random.uniform(10, 30)
        fat_percent = random.uniform(20, 40)
        carbs_percent = 100 - protein_percent - fat_percent
        
        # Calculate protein, fat, and carbs based on TDEE and macronutrient percentages
        protein = int(tdee * (protein_percent / 100) / 4)  # 4 calories per gram of protein
        fat = int(tdee * (fat_percent / 100) / 9)  # 9 calories per gram of fat
        carbs = int(tdee * (carbs_percent / 100) / 4)  # 4 calories per gram of carbs
        
        # Generate meal preference with at least one macronutrient restriction
        meal_preference = random.sample(["high_protein", "low_sugar", "gluten_free", "dairy_free", "low_carb", "keto"], k=2)
        
        # Calculate max energy per meal based on typical meal frequency
        meal_frequency = random.choice([1, 1.2, 2, 2.2, 3, 3.2])  # typical meal frequency
        max_energy_per_meal = int(tdee / meal_frequency)
        
        # Create the user profile
        profile = {
            "id": index + 1,
            "total_energy_expenditure": tdee,
            "diet_preference": random.choice(["omnivore", "vegan", "vegetarian", "pescetarian", "paleo"]),
            "meal_preference": meal_preference,
            "max_energy_per_meal": max_energy_per_meal,
            "protein": protein,
            "fat": fat,
            "carbs": carbs,
            "allergens": ', '.join(random.choices(food_allergens, k=random.randint(0, 2)))
        }
        user_profiles_data.append(profile)
    return pd.DataFrame(user_profiles_data)

# Generate and save user profiles to CSV
user_profiles_df = generate_user_profile(100)
user_profiles_df.to_csv('user_profiles.csv', index=False)

print("Generated user profiles are saved in user_profiles.csv")