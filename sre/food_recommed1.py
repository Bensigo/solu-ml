import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os


# Function to derive nutritional goals based on user profile and health status
def derive_nutritional_goals(user_profile):
    # Baseline nutritional goals (based on dietary guidelines)
    baseline_nutrition = {
        "calories": 2000,
        "protein": 60,  # in grams
        "carbs": 300,   # in grams
        "fat": 50       # in grams
    }

    # Adjust nutritional goals based on user profile and health status
    # For simplicity, we'll use some basic assumptions here
    # You would typically calculate these values based on more detailed factors
    if user_profile["gender"] == "female":
        baseline_nutrition["calories"] -= 100  # Adjust for lower calorie needs
        baseline_nutrition["protein"] -= 5     # Adjust for lower protein needs
    if user_profile["activity_level"] == "active":
        baseline_nutrition["calories"] += 200  # Adjust for higher calorie needs

    # Adjust nutritional goals based on diet preferences
    if user_profile["diet_preference"] == "vegan":
        # Increase protein and fat goals for vegan diet
        baseline_nutrition["protein"] += 10
        baseline_nutrition["fat"] += 10
    elif user_profile["diet_preference"] == "pescatarian":
        # Increase protein goal for pescatarian diet
        baseline_nutrition["protein"] += 5

    # Adjust nutritional goals based on health conditions (e.g., diabetes, hypertension)
    for condition in user_profile["health_conditions"]:
        if condition == "diabetes":
            # Reduce carbs goal for diabetes management
            baseline_nutrition["carbs"] -= 50
        elif condition == "hypertension":
            # Reduce sodium intake for hypertension management
            # Adjust other nutritional goals as needed for specific health conditions
            pass

    return baseline_nutrition

# Function to filter recipes based on user preferences and health goals
def filter_recipes(recipes_df, user_preferences):
    # Filter recipes based on favorite ingredients
    filtered_recipes = recipes_df[recipes_df["RecipeIngredientParts"].apply(lambda x: all(ingredient in x for ingredient in user_preferences["favorite_ingredients"]))]

    return filtered_recipes

# Function to recommend recipes based on user preferences
#def recommend_recipes(user_preferences, filtered_recipes):
    # Calculate cosine similarity between user preferences and recipe nutritional information
#    recipe_nutrition = np.array(filtered_recipes[["Calories", "ProteinContent", "CarbohydrateContent", "FatContent"]])
#    user_nutrition = np.array([user_preferences["nutritional_goals"]["calories"],
#                               user_preferences["nutritional_goals"]["protein"],
#                              user_preferences["nutritional_goals"]["carbs"],
#                               user_preferences["nutritional_goals"]["fat"]])
#    similarities = cosine_similarity(recipe_nutrition, [user_nutrition])
#
#    # Sort recipes by similarity score
#    recommended_recipes = filtered_recipes.copy()
#    recommended_recipes["similarity"] = similarities
#    recommended_recipes = recommended_recipes.sort_values(by="similarity", ascending=False)

#    return recommended_recipes

def recommend_recipes(user_preferences, filtered_recipes):
    if filtered_recipes.empty:
        #print("No recipes match the user's preferences.")
        return pd.DataFrame()  # Return an empty DataFrame if no recipes match

    # Calculate cosine similarity between user preferences and recipe nutritional information
    recipe_nutrition = np.array(filtered_recipes[["Calories", "ProteinContent", "CarbohydrateContent", "FatContent"]])
    user_nutrition = np.array([user_preferences["nutritional_goals"]["calories"],
                               user_preferences["nutritional_goals"]["protein"],
                               user_preferences["nutritional_goals"]["carbs"],
                               user_preferences["nutritional_goals"]["fat"]])
    
    similarities = cosine_similarity(recipe_nutrition, [user_nutrition])

     

    # Sort recipes by similarity score
    recommended_recipes = filtered_recipes.copy()
    recommended_recipes["similarity"] = similarities
    recommended_recipes = recommended_recipes.sort_values(by="similarity", ascending=False)

    return recommended_recipes


# Function to provide contextual recommendations based on time of day
#def contextual_recommendations(recommended_recipes):
    # Since we don't have tags for time of day, returning top recommendations directly
#    return recommended_recipes.head(5)

# Main function to recommend recipes
#def recommend(user_profile, recipes_df):
#    user_preferences = {
#        "favorite_ingredients": ["chicken", "vegetables", "rice"],
#        "allergies": ["nuts", "shellfish"],
#        "dietary_restrictions": ["gluten-free"],
#        "nutritional_goals": derive_nutritional_goals(user_profile)
#    }

#    filtered_recipes = filter_recipes(recipes_df, user_preferences)
#    recommended_recipes = recommend_recipes(user_preferences, filtered_recipes)
#    contextual_recommendations = contextual_recommendations(recommended_recipes)
#    return contextual_recommendations

# Function to provide contextual recommendations based on time of day
def get_contextual_recommendations(recommended_recipes):
    # Since we don't have tags for time of day, returning top recommendations directly
    return recommended_recipes.head(5)

# Main function to recommend recipes
def recommend(user_profile, recipes_df):
    user_preferences = {
        "favorite_ingredients": ["chicken", "vegetables", "rice"],  # why do we have this here
        "allergies": ["nuts", "shellfish"],
        "dietary_restrictions": ["gluten-free"],
        "nutritional_goals": derive_nutritional_goals(user_profile)
    }

    filtered_recipes = filter_recipes(recipes_df, user_preferences)
    recommended_recipes = recommend_recipes(user_preferences, filtered_recipes)
    contextual_recommendations = get_contextual_recommendations(recommended_recipes)
    return contextual_recommendations






def main ():
    path_to_save = os.path.join("datasets", "sampled_dataset.csv")
    file_exist = os.path.exists(path_to_save)

    if file_exist == False:
        print("failed to find file")
        return
    

    # Load the recipe dataset
    recipes_df = pd.read_csv(path_to_save)

    # Sample user profile including diet preference and health status
    user_profile = {
        "diet_preference": "omnivore",  # Possible values: vegan, vegetarian, omnivore, pescatarian, etc.
        "age": 30,
        "gender": "female",
        "weight_kg": 65,
        "height_cm": 170,
        "activity_level": "moderate",  # Possible values: sedentary, low_active, active, very_active, etc.
        "health_conditions": []  # List of health conditions, e.g., "diabetes", "hypertension"
    }
    # print(recipes_df.head())
    # Example of recommending recipes for the user
    recommended_recipes = recommend(user_profile, recipes_df)

    # Check if there are recommendations available
    if not recommended_recipes.empty:
        print(recommended_recipes[["Name", "Calories", "ProteinContent", "CarbohydrateContent", "FatContent"]])
    else:
        print("No recipes match the user's preferences.")


main()


