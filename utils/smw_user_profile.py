from utils.helpers import  calculate_stress



# class SMW_USER_PROFILE:
#     fitness_goal: str
#     age: int
#     sleeping_time: int
#     steps_count: int
#     heart_rates: List[float]
       

# PAL_MAPPING = {
#         "sedentary": 0,
#         "lightly_active": 1,
#         "moderately_active": 2,
#         "very_active": 3,
#         "extremely_active": 4
# }

# def create_smw_user_profile(data):
#     fitness_goal = data['fitness_goal']
#     steps_count = data['steps_count']
#     sleep_count = data['sleeping_time']

#     age = data['age']
#     if steps_count < 5000:
#         pal = PAL_MAPPING["sedentary"]
#     elif steps_count < 7500:
#         pal = PAL_MAPPING["lightly_active"]
#     elif steps_count < 10000:
#         pal = PAL_MAPPING["moderately_active"]
#     elif steps_count < 12500:
#         pal = PAL_MAPPING["very_active"]
#     else:
#         pal = PAL_MAPPING["extremely_active"]
    
#     hrvs = data.get('hrvs', [])
#     hrv = data.get('hrv', [])
    
#     if not hrvs:
#         # Handle case where HRV data is missing or empty
#         return {
#             "fitness_goal": [fitness_goal],
#             "age":[age],  
#             "sleep_count": [sleep_count],
#             "fitness_level": [pal],
#             "stress_level": [0]
#         }
    
#     min_hrv = min(hrvs)
#     max_hrv = max(hrvs)
#     low_threshold = 20  # to change data from expert
#     high_threshold = 60 # to change  data from expert


#     stress_level = calculate_stress(hrv, min_hrv, max_hrv, low_threshold, high_threshold)
    

#     return {
#         "fitness_goal": [fitness_goal],
#         "age": [age],  
#         "sleep_count": [sleep_count],
#         "fitness_level": [pal],
#         "stress_level": [stress_level]
#     }



PAL_MAPPING = {
    "sedentary": 0,
    "lightly_active": 1,
    "moderately_active": 2,
    "very_active": 3,
    "extremely_active": 4
}

def calculate_hrv_thresholds(age, fitness_level='average', health_condition=None):
    # Define baseline HRV ranges based on age and fitness level
    age_ranges = {
        'young_adult': (20, 40),
        'middle_adult': (41, 60),
        'older_adult': (61, 100)
    }
    
    fitness_levels = {
        'sedentary': (-1, 1),
        'average': (0, 2),
        'athletic': (1, 3)
    }

    # Define adjustments based on health conditions
    health_condition_adjustments = {
        'high_stress': -0.5,
        'low_stress': 0.5,
        'health_condition': 0  # Placeholder for other health conditions
    }

    # Determine age range
    if age <= 40:
        age_range = 'young_adult'
    elif age <= 60:
        age_range = 'middle_adult'
    else:
        age_range = 'older_adult'

    # Determine fitness level range
    fitness_range = fitness_levels.get(fitness_level, (0, 2))  # Default to average

    # Apply adjustments based on health condition
    health_adjustment = health_condition_adjustments.get(health_condition, 0)

    # Calculate low and high thresholds
    low_threshold = age_ranges[age_range][0] + fitness_range[0] + health_adjustment
    high_threshold = age_ranges[age_range][1] + fitness_range[1] + health_adjustment

    return low_threshold, high_threshold

def create_smw_user_profile(data):
    fitness_goal = data['fitness_goal']
    steps_count = data['steps_count']
    sleep_count = data['sleeping_time']
    age = data['age']
    
    # Determine Physical Activity Level (PAL)
    if steps_count < 5000:
        pal = PAL_MAPPING["sedentary"]
    elif steps_count < 7500:
        pal = PAL_MAPPING["lightly_active"]
    elif steps_count < 10000:
        pal = PAL_MAPPING["moderately_active"]
    elif steps_count < 12500:
        pal = PAL_MAPPING["very_active"]
    else:
        pal = PAL_MAPPING["extremely_active"]
    
    hrvs = data.get('hrvs', [])
    hrv = data.get('hrv', [])
    
    if not hrvs:
        # Handle case where HRV data is missing or empty
        return {
            "fitness_goal": [fitness_goal],
            "age": [age],  
            "sleep_count": [sleep_count],
            "fitness_level": [pal],
            "stress_level": [0]
        }
    
    min_hrv = min(hrvs)
    max_hrv = max(hrvs)
    
    # Calculate low and high thresholds dynamically
    low_threshold, high_threshold = calculate_hrv_thresholds(age, PAL_MAPPING.inverse[pal])  # Inverse mapping of PAL
    
    stress_level = calculate_stress(hrv, min_hrv, max_hrv, low_threshold, high_threshold)
    
    return {
        "fitness_goal": [fitness_goal],
        "age": [age],  
        "sleep_count": [sleep_count],
        "fitness_level": [pal],
        "stress_level": [stress_level]
    }

