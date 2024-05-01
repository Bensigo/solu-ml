import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
recipes_df = pd.read_csv('recipes.csv')
user_profiles_df = pd.read_csv('user_profiles.csv')

# Inspect the first few rows
print(recipes_df.head())
print(user_profiles_df.head())

# Statistical summary
# print(recipes_df.describe())
# print(user_profiles_df.describe())

# Correlation analysis for user profiles
correlation_matrix = user_profiles_df[['total_energy_expenditure', 'max_energy_per_meal', 'protein', 'fat', 'carbs']].corr()
# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix of User Profile Features')
plt.show()


# Consistency checks for recipes and allergens
# def check_allergens(row):
#     # Convert NaN to empty string before split
#     ingredients = set(row['ingredients'].split(', '))
#     allergens = row['allergens']
#     if pd.isna(allergens):
#         allergens = ''
#     allergens = set(allergens.split(', '))
#     return allergens.isdisjoint(ingredients)

# recipes_df['is_consistent'] = recipes_df.apply(check_allergens, axis=1)
# print(f"Inconsistent recipes: {recipes_df[~recipes_df['is_consistent']].shape[0]}")

# # # Validate nutrient fields
# recipes_df[['protein', 'fat', 'carbs']].plot(kind='box')
# plt.show()