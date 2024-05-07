import numpy as np
import pandas as pd
import datetime
from sklearn.metrics.pairwise import euclidean_distances

from utils.supabase import recipe_table

# Data preparation and cleaning
def prepare_data(data):
    data = data.fillna(method='ffill')  # Example: fill missing values
    return data

# Filter recipes based on user profile
def filter_recipes(recipes, user_profile):
    # Filtering by allergies, diet, and meal preferences
    if user_profile['allergies']:
        user_allergies = user_profile['allergies']
        recipes = recipes[~recipes['allergens'].apply(lambda x: any(allergie in x for allergie in user_allergies))]
    if user_profile['diet_preference'] :
        recipes = recipes[recipes['dietType'] == user_profile['diet_preference']]
    if user_profile['meal_preference']:
        user_pref = user_profile['meal_preference']
        recipes = recipes[recipes['mealPreference'].apply(lambda x: any(pref in x for pref in user_pref))]

    # Calorie-based filtering
    max_energy = user_profile['max_energy_per_meal']
    recipes = recipes[(recipes['calories'] >= max_energy * 0.9) & (recipes['calories'] <= max_energy * 1.1)]
    return recipes

# Calculate Euclidean distance for nutrient profiles
def calculate_similarity(user_profile, recipes):
    if recipes.empty or 'nutrients' not in recipes.columns:
        print("No nutrients available in recipes.")
        return None

    # Extract nutrients from recipes
    nutrients = recipes['nutrients']

    # Initialize variables for nutrients
    carbs = [float(nutrient['value']) for nutrient_list in nutrients for nutrient in nutrient_list if nutrient['name'].lower() == 'carbs']
    protein = [float(nutrient['value']) for nutrient_list in nutrients for nutrient in nutrient_list if nutrient['name'].lower() == 'protein']
    fat = [float(nutrient['value']) for nutrient_list in nutrients for nutrient in nutrient_list if nutrient['name'].lower() == 'fat']
 
    # Extract calories
    calories = recipes['calories']

    # Construct nutrient arrays
    user_nutrients = np.array([user_profile['nutrients']['protein'], user_profile['nutrients']['fat'], user_profile['nutrients']['carbs'], user_profile['max_energy_per_meal']])
    recipe_nutrients = np.array([protein, fat, carbs, calories]).T  # Transpose for correct shape

    # Compute Euclidean distances
    distances = euclidean_distances(user_nutrients.reshape(1, -1), recipe_nutrients)

    # Add distances as a new column in recipes
    recipes['distance'] = distances[0]
    return recipes



# Determine meal type based on current time
def contextual_recommendation(recipes):
    current_time = datetime.datetime.now().hour
    if current_time < 10:
        meal_type = 'breakfast'
    elif current_time < 16:
        meal_type = 'lunch'
    else:
        meal_type = 'dinner'
    
    filtered_recipes = recipes[(recipes['mealType'].lower() == meal_type) | (recipes['mealType'].lower() == 'snack')]
    return filtered_recipes

# Combine everything into a recommendation pipeline
def recommend_recipes(user_profile, recipes):
    # recipes = prepare_data(recipes)
    recipes = filter_recipes(recipes, user_profile)
    recipes = calculate_similarity(user_profile, recipes)
    # recipes = contextual_recommendation(recipes)
    
    # Sort recipes by distance, lower distance means more similar
    sorted_recipes = recipes.sort_values(by='distance', ascending=True)

    # Select the top 10 recommendations
    top_recipes = sorted_recipes.head(10)
    return top_recipes

# User profile example
user_profile = {
    "total_energy_expenditure": 2200,
    "diet_preference": ["vegan"],
    "meal_preference": [],
    "max_energy_per_meal": 600,
    "nutrients": {"protein": 75, "fat": 40, "carbs": 150},
    "allergies": [],
    # future plan 
    "cusineType": ["mexican", "African", "Thai"]

}

def main():
    # recipes = pd.read_csv('recipes.csv')
    resp = recipe_table.select('*').execute()
    recipes = pd.DataFrame(resp.data)
    recommended_recipes = recommend_recipes(user_profile, recipes)
    print(recommended_recipes)

if __name__ == "__main__":
    main()