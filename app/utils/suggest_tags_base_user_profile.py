from utils.tags import  age_ranges


def get_age_range(age):
    for age_range in age_ranges:
        start, end = map(int, age_range.split('-'))
        if start <= age <= end:
            return age_range
    return None 

def suggest_tags_with_weights(user_profile, tags):
    tag_weights = {
        # Weightage for age groups
        '18-22': 2, '23-27': 2, '28-32': 2, '33-37': 2, '38-42': 2, '43-47': 2, '48-52': 2, '53-57': 2, '58-62': 2, '63-67': 2,
        
        # Weightage for diet preferences
        "vegan": 3, "vegetarian": 3, "omnivore": 3, "pescatarian": 3, "paleo": 2,
        "keto": 2, "gluten_free": 2, "dairy_free": 2,
        "low_carb": 1, "low_fat": 1, "low_sugar": 1, "high_protein": 1,
        "organic": 1, "raw_food": 1, "whole30": 1, "flexitarian": 1,
        
        # Weightage for fitness goals
        "weight_loss": 3, "muscle_gain": 3, "endurance": 3, "flexibility": 3, "stress_relief": 3,
        
        # Weightage for activity level
        "sedentary": 2, "low_active": 2, "active": 3, "very_active": 3,
        
        # Weightage for health conditions
        "diabetes": 2, "hypertension": 2, "high_cholesterol": 2, "heart_disease": 2,
        "arthritis": 1, "allergies": 1, "asthma": 1,
        
        # Weightage for sleep quality
        "poor_sleep": 2, "good_sleep": 2, "fair_sleep": 1,
        
        # Weightage for stress level
        "low_stress": 2, "moderate_stress": 2, "high_stress": 3
    }

    tag_scores = {}

    # Diet preferences
    diet_preference = user_profile.get("diet_preference", "")
    if diet_preference in tags:
        tag_scores[diet_preference] = tag_weights.get(diet_preference, 1)
    
    # meal preferences
    meal_preferences = user_profile.get("meal_preference", [])
    for preference in meal_preferences:
        if preference in tags:
            tag_scores[preference] = tag_weights.get(preference, 1)

    # Fitness goals
    fitness_goal = user_profile.get("fitness_goal", "")
    if fitness_goal in tags:
        tag_scores[fitness_goal] = tag_weights.get(fitness_goal, 1)

    # Age
    age = user_profile.get("age", 0)
  
    if age in tags:
        tag_scores[age] = tag_weights.get(age, 1)

    # Activity level
    activity_level = user_profile.get("activity_level", "")
    if activity_level in tags:
        tag_scores[activity_level] = tag_weights.get(activity_level, 1)

    # Health conditions (if any)
    health_conditions = user_profile.get("health_conditions", [])
    for condition in health_conditions:
        if condition in tags:
            tag_scores[condition] = tag_weights.get(condition, 1)

    # Sleep
    sleeping_time = user_profile.get("sleeping_time(mins)", 0)
    if sleeping_time < 360:
        tag = "poor_sleep"
    elif sleeping_time >= 480:
        tag = "good_sleep"
    else:
        tag = "fair_sleep"
    if tag in tags:
        tag_scores[tag] = tag_weights.get(tag, 1)

    # Stress level
    stress_level = user_profile.get("stress_level", 0)
    if stress_level == 0:
        tag = "low_stress"
    elif stress_level == 1:
        tag = "moderate_stress"
    else:
        tag = "high_stress"
    if tag in tags:
        tag_scores[tag] = tag_weights.get(tag, 1)

    # Sort tags by weight
    sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)

    # Return suggested tags
    return [tag[0] for tag in sorted_tags[:8]]