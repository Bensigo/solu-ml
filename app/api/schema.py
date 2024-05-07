from pydantic import BaseModel
from typing import List
from fastapi import   Body


class Recipe_User_Profile(BaseModel):
    age: int
    gender: str
    height: int
    weight: int
    step_count: int
    diet_preference: str
    fitness_goal: str
    meal_preference: List[str]
    meal_frequency: float
    allergies: List[str]

  # input_data = {
    #   'fitness_goal': ['muscle_gain'],
    #   'age': [48],
    #   'sleeping_hours': [7.5],
    #   'steps_count': [19200],
    #   'fitness_level': [1],
    #   'stress_level': [1]
 # }

class SMW_USER_PROFILE(BaseModel):
    fitness_goal: str
    age: int
    sleeping_time: int
    steps_count: int
    hrvs: List[float]
    hrv: float



class Recipe_Req_Body(BaseModel):
    age: int = Body(..., description="Age of the user")
    gender: str = Body(..., description="Gender of the user")
    height: int = Body(..., description="Height of the user")
    weight: int = Body(..., description="Weight of the user")
    step_count: int = Body(..., description="Step count of the user")
    diet_preference: str = Body(..., description="Diet preference of the user")
    fitness_goal: str = Body(..., description="Fitness goal of the user")
    meal_preference: List[str] = Body(..., description="Meal preference of the user")
    meal_frequency: float = Body(..., description="Meal frequency of the user")
    allergies: List[str] = Body(..., description="Allergies of the user")


class SMW_Req_Body(BaseModel):
    fitness_goal: str = Body(..., description="Fitness goal of the user")
    age: int = Body(..., description="Age of the user")
    sleeping_time: int = Body(..., description="Sleeping time in mins")
    steps_count: int = Body(..., description="Step count of the user")
    hrvs: List = Body(..., description="HRVs of the user")
    hrv: float = Body(..., description="HRV of the user")


