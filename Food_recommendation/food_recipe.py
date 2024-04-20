# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 13:34:10 2024

@author: Oghale Enwa
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load the dataset
def load_dataset(file_path):
    recipes_df = pd.read_csv(file_path)
    return recipes_df

# Function to remove foods that the user is allergic to
def remove_allergens(recipes_df, user_profile):
    user_allergies = user_profile.get("allergies", [])
    for allergy in user_allergies:
        recipes_df = recipes_df[~recipes_df["RecipeIngredientParts"].str.contains(allergy, case=False)]
    return recipes_df

# Function to perform TF-IDF vectorization
def perform_tfidf(recipes):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(recipes["RecipeIngredientParts"])
    return tfidf_matrix, tfidf_vectorizer

# Function to calculate cosine similarity between recipes
def calculate_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend meals based purely on nutritional matching
def recommend_meals(recipes_df, cosine_sim, user_profile):
    nutritional_goals = derive_nutritional_goals(user_profile)
    recommended_meals = {}
    for idx, row in recipes_df.iterrows():
        if (row['Calories'] <= nutritional_goals['calories'] and
            row['ProteinContent'] >= nutritional_goals['ProteinContent'] and
            row['FatContent'] <= nutritional_goals['FatContent'] and
            row['CarbohydrateContent'] <= nutritional_goals['CarbohydrateContent']):
            recommended_meals[idx] = row.to_dict()
            if len(recommended_meals) >= 5:  # Limit to top 5 recommendations
                break
    return recommended_meals

# Function to derive nutritional goals based on user profile and health status
def derive_nutritional_goals(user_profile):
    # Pull nutrition directly from profile
    return user_profile["nutrition"]

# Function to display recommended meals
def display_recommended_meals(filtered_meals, meal_type):
    print("Top 5 Recommended", meal_type + "s" + ":")
    for idx, meal_recipe in filtered_meals.head(5).iterrows():
        print(meal_recipe["Name"])
        print("Ingredients:", meal_recipe["RecipeIngredientParts"])
        print()

# Main function
def main():
    # Load dataset
    recipes_df = load_dataset("sampled_dataset.csv")

    # User profile with allergies and nutrition details
    user_profile = {
        "gender": "female",
        "activity_level": "active",
        "diet_preference": "vegan",
        "health_conditions": ["hypertension"],
        "allergies": ["peanuts", "shellfish"],
        "nutrition": {
            "calories": 998,  # Adjusted for active lifestyle
            "ProteinContent": 70,  # Increased for vegan diet
            "CarbohydrateContent": 300,
            "FatContent": 60
        }
    }

    # Remove allergens
    recipes_df = remove_allergens(recipes_df, user_profile)

    # TF-IDF Vectorization
    tfidf_matrix, tfidf_vectorizer = perform_tfidf(recipes_df)

    # Calculate cosine similarity
    cosine_sim = calculate_similarity(tfidf_matrix)

    # Recommend meals based on nutritional matching
    recommended_meals = recommend_meals(recipes_df, cosine_sim, user_profile)

    # Convert to DataFrame for easy handling
    recommended_meals_df = pd.DataFrame.from_dict(recommended_meals, orient='index')

    # Display recommended meals
    display_recommended_meals(recommended_meals_df, "Meal")

if __name__ == "__main__":
    main()
