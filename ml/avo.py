

"diet_preference": "omnivore",
"age": 30,
"fitness_goal": "weight_loss",
"activity_level": "low_active",
"meal_preference": ["high_protein", "low_sugar", "gluten_free"],
"health_conditions": [],
"sleeping_time(mins)": 170,
"steps_count": 4000,
"stress_level": 1,
"height": 164,
"weight" : 65


User Profile Data structure  
diet_preference: ["omnivore", "vegan", "Vegetarian", "Pescetarian", "Paleo"]
age: 0-60
fitness_goal: ["Weight loss", "Muscle gain", "Endurance improvement", "Stress relief", "Mobility Improvement"]
meal_preference: ["high_protein", "low_sugar", "gluten_free", "Dairy free", "Low carb", "Keto"] 
allegies: [] # recipe should now have any ingredient allegies,
height(cm): 0-200
weight(kg): 0-200,
step_count: 0-20000 # use to calucalate the activity level of the user,
meal_frequency: [1, 1.2, 2, 2.2, 3, 3.2]


response 
{
    total_enegry_expenditure,
    diet_preference,
    fitness_goal, 
    meal_preference,
    max_energy_per_meal,
    nutrients
    allegies
}



