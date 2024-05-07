import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Read the food recipes dataset
path_to_save = os.path.join("datasets", "sampled_dataset.csv")

recipes_df = pd.read_csv(path_to_save)




# Sample user information
user_allergies = ["peanuts", "shellfish"]
user_likes = ["chicken", "broccoli"]  # I think this  come in later base on data will collect later
user_fitness_level = "high"  # Options: "low", "medium", "high"

# Remove foods that the user is allergic to
for allergy in user_allergies:
    recipes_df = recipes_df[~recipes_df["RecipeIngredientParts"].str.contains(allergy, case=False)]

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(recipes_df["RecipeIngredientParts"])

# Calculate cosine similarity between recipes
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get top N similar recipes
def get_top_similar_recipes(recipe_index, n=5):
    sim_scores = list(enumerate(cosine_sim[recipe_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar_recipes = sim_scores[1:n+1]  # Exclude itself
    return top_similar_recipes

# Recommend meals based on user preferences and similarity between recipes
def recommend_meals(user_likes, user_fitness_level):
    recommended_meals = {}
    for like in user_likes:
        like_indices = recipes_df.index[recipes_df["RecipeIngredientParts"].str.contains(like, case=False)]
        for idx in like_indices:
            top_similar = get_top_similar_recipes(idx)
            for sim_idx, sim_score in top_similar:
                if recipes_df.index[sim_idx] not in recommended_meals:
                    recommended_meals[idx] = recipes_df.iloc[sim_idx]
                    break
            if idx in recommended_meals:
                break
    return recommended_meals

# Filter recipes based on user's provided health/fitness level
def filter_by_fitness_level(recipes_df, user_fitness_level):
    if user_fitness_level == "low":
        return recipes_df[recipes_df["Calories"] < 500]
    elif user_fitness_level == "medium":
        return recipes_df[recipes_df["Calories"] < 400]
    elif user_fitness_level == "high":
        return recipes_df[recipes_df["Calories"] < 300]

# Get recommended meals
recommended_meals = recommend_meals(user_likes, user_fitness_level)

# Filter recommended meals based on fitness level
recommended_meals_df = pd.DataFrame.from_dict(recommended_meals, orient='index')
filtered_meals = filter_by_fitness_level(recommended_meals_df, user_fitness_level)

# Display top 5 recommended meals for each meal type
for meal_type in ["Breakfast", "Lunch", "Dinner"]:
    print("Top 5 Recommended", meal_type + "s" + ":")
    if meal_type == "Breakfast":
        filtered_by_type = filtered_meals[filtered_meals["PrepTime"] < 30]
    elif meal_type == "Lunch":
        filtered_by_type = filtered_meals[(filtered_meals["PrepTime"] >= 30) & (filtered_meals["PrepTime"] < 60)]
    else:
        filtered_by_type = filtered_meals[filtered_meals["PrepTime"] >= 60]
    for idx, meal_recipe in filtered_by_type.head(5).iterrows():
        print(meal_recipe["Name"])
        print("Ingredients:", meal_recipe["RecipeIngredientParts"])
        print()
