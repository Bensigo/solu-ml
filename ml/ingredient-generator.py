import pandas as pd
from pulp import *  # Import all to ensure we aren't missing any components

def generate_ingredients_for_calories(target_calories, file_path):
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Clean and prepare the data
    data['Cals_per100grams'] = data['Cals_per100grams'].str.replace(' cal', '').astype(float)
    data = data[data['Cals_per100grams'] > 0]  # Ensuring all items have positive calorie values

    # Setup the problem
    problem = LpProblem("Ingredient_Selection", LpMinimize)

    # Define decision variables for ingredient amounts (grams)
    amounts = LpVariable.dicts("Amount", data.index, lowBound=0, upBound=100, cat='Continuous')  # Max 100 grams of any ingredient

    # Objective: Minimize total calorie intake
    problem += lpSum(amounts[i] * data.loc[i, 'Cals_per100grams'] for i in data.index)

    # Constraint: ensure caloric intake does not exceed the target
    problem += lpSum(amounts[i] * data.loc[i, 'Cals_per100grams'] for i in data.index) <= target_calories

    # Constraint: at least some minimal use of ingredients, enforce sum of weights to be greater than zero
    problem += lpSum(amounts[i] for i in data.index) >= 1  # Avoid trivial all-zero solutions

    # Solve the problem
    problem.solve()

    # Output results
    if LpStatus[problem.status] == 'Optimal':
        print("Optimal Solution Found:\n")
        for var in amounts:
            if amounts[var].varValue > 0:
                print(f"{data.loc[var, 'FoodItem']} : {round(amounts[var].varValue, 2)} grams")
    else:
        print(f"No optimal solution. Status: {LpStatus[problem.status]}")


if __name__ == "__main__":
    target_calories = float(input("Enter target calorie amount: "))
    file_path = 'calories.csv'  # Update it to the path where your CSV file is stored.
    generate_ingredients_for_calories(target_calories, file_path)