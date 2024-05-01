from utils.helpers import  calculate_stress



# class SMW_USER_PROFILE:
#     fitness_goal: str
#     age: int
#     sleeping_time: int
#     steps_count: int
#     heart_rates: List[float]
       

PAL_MAPPING = {
        "sedentary": 0,
        "lightly_active": 1,
        "moderately_active": 2,
        "very_active": 3,
        "extremely_active": 4
}

def create_smw_user_profile(data):
    fitness_goal = data['fitness_goal']
    steps_count = data['steps_count']
    sleep_count = data['sleeping_time']

    age = data['age']
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
            "age":[age],  
            "sleep_count": [sleep_count],
            "fitness_level": [pal],
            "stress_level": [0]
        }
    
    min_hrv = min(hrvs)
    max_hrv = max(hrvs)
    low_threshold = 20  # to change data from expert
    high_threshold = 60 # to change  data from expert


    stress_level = calculate_stress(hrv, min_hrv, max_hrv, low_threshold, high_threshold)
    

    return {
        "fitness_goal": [fitness_goal],
        "age": [age],  
        "sleep_count": [sleep_count],
        "fitness_level": [pal],
        "stress_level": [stress_level]
    }
