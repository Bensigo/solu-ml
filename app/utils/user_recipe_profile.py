
def generate_user_profile_for_recipe(user_profile):
    PAL_MAPPING = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extremely_active": 1.9
    }
    # Constants for calculating total energy expenditure
    CALORIES_PER_GRAM_PROTEIN = 4
    CALORIES_PER_GRAM_CARBS = 4
    CALORIES_PER_GRAM_FAT = 9
    
    # Extract user profile data
    age = user_profile["age"]
    gender = user_profile["gender"]
    height = user_profile["height"]
    weight = user_profile["weight"]
    step_count = user_profile["step_count"]
    meal_frequency = user_profile["meal_frequency"]
    fitness_goal = user_profile['fitness_goal']
    meal_preference = user_profile["meal_preference"]
    
    # Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation
    if gender == "male":
        bmr = round((10 * weight) + (6.25 * height) - (5 * age) + 5, 2)
    else:
        bmr = round((10 * weight) + (6.25 * height) - (5 * age) - 161, 2)
    
    # Calculate Physical Activity Level (PAL) based on step count
    if step_count < 5000:
        pal = PAL_MAPPING["sedentary"]
    elif step_count < 7500:
        pal = PAL_MAPPING["lightly_active"]
    elif step_count < 10000:
        pal = PAL_MAPPING["moderately_active"]
    elif step_count < 12500:
        pal = PAL_MAPPING["very_active"]
    else:
        pal = PAL_MAPPING["extremely_active"]
    
    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = round(bmr * pal, 2)
    print("first: ", tdee)
    if fitness_goal.lower() == "weight loss":
        tdee *= 0.8
    elif fitness_goal.lower() == "muscle gain":
        tdee *= 1.2
    
    # Adjust nutrient composition based on meal preference
    if "high protein" in meal_preference:
        protein_ratio = 0.4
        carbs_ratio = 0.25
        fat_ratio = 0.3
    elif "low carb" in meal_preference or "keto" in meal_preference:
        protein_ratio = 0.3
        carbs_ratio = 0.2
        fat_ratio = 0.5
    else:
        # Default nutrient ratios if no specific meal preference is provided
        protein_ratio = 0.25
        carbs_ratio = 0.5
        fat_ratio = 0.25
    
    # Calculate nutrient intake based on adjusted ratios
    nutrients = {
        "protein": round(weight * protein_ratio, 2),
        "carbs": round(tdee * carbs_ratio / CALORIES_PER_GRAM_CARBS, 2),
        "fat": round(tdee * fat_ratio / CALORIES_PER_GRAM_FAT, 2)
    }
    
    # Generate response
    response = {
        "total_energy_expenditure": tdee,
        "diet_preference": user_profile["diet_preference"],
        "meal_preference": meal_preference,
        "max_energy_per_meal": round(tdee / meal_frequency, 2),
        "nutrients": nutrients,
        "allergies": user_profile["allergies"]
    }
    
    return response
  

# Example usage:
# user_profile = {
#     "age": 30,
#     "gender": "female",
#     "height": 165,
#     "weight": 68,
#     "step_count": 4000,
#     "diet_preference": "omnivore",
#     "fitness_goal": "weight_loss",
#     "meal_preference":  ["high_protein"],
#     "meal_frequency": 2.2,
#     "allergies": ["black pepper"]
# }

# response = generate_user_profile_for_recipe(user_profile)
# print(response)
