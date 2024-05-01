import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Custom transformer for selecting dataframe columns
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names]

# Custom transformer for properly selecting text data for TfidfVectorizer
class TextSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key].values  # Ensure it returns a 1D array suitable for TfidfVectorizer

def load_data(user_filepath, recipe_filepath):
    user_df = pd.read_csv(user_filepath)
    recipe_df = pd.read_csv(recipe_filepath)
    return user_df, recipe_df

def create_feature_pipeline():
    numeric_attributes = ['calories', 'protein', 'fat', 'carbs']
    categorical_attributes = ['diet_preference']
    text_attribute = 'description'
    
    numeric_pipeline = Pipeline([
        ('selector', DataFrameSelector(numeric_attributes)),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_pipeline = Pipeline([
        ('selector', DataFrameSelector(categorical_attributes)),
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    text_pipeline = Pipeline([
        ('selector', TextSelector(text_attribute)),
        ('tfidf', TfidfVectorizer(max_features=100))
    ])
    
    full_pipeline = FeatureUnion([
        ('numeric', numeric_pipeline),
        ('categorical', categorical_pipeline),
        ('text', text_pipeline)
    ])
    
    return full_pipeline

def train_and_evaluate(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))
    return model

def main(user_csv, recipe_csv):
    user_df, recipe_df = load_data(user_csv, recipe_csv)

    # Check columns
    print("User DataFrame Columns:", user_df.columns)
    print("Recipe DataFrame Columns:", recipe_df.columns)

    pipeline = create_feature_pipeline()
    features = pipeline.fit_transform(recipe_df)
    target = np.random.randint(0, 2, size=len(recipe_df))  # Generate dummy target data for demonstration

    model = train_and_evaluate(features, target)



if __name__ == "__main__":
    main('./utils/faker/user_profiles.csv', './utils/faker/recipes.csv')