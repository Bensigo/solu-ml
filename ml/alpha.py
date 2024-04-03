import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os



# Define ranges for input features
fitness_goals = ['weight_loss', 'muscle_gain', 'endurance', 'flexibility', 'stress_relief']
age_range = (18, 80)
sleeping_hours_range = (4, 10)
steps_count_range = (0, 20000)
fitness_level_range = (0, 3)
stress_level_range = (0, 2)

# Define labels for suggested output
fitness_categories = ['cardiovascular', 'HIIT', 'muscle_training',
                      'strength', 'endurance', 'mobility', 'therapy', 'mindfulness']



# Define rules to assign labels based on input features
# def assign_labels(fitness_goal, age, sleeping_hours, steps_count, fitness_level, stress_level):
#     labels = []
#     if fitness_goal == 'weight_loss':
#         labels.extend(['cardiovascular', 'HIIT', 'strength', 'endurance'])
#     elif fitness_goal == 'muscle_gain':
#         labels.extend(['muscle_training', 'strength'])
#     elif fitness_goal == 'endurance':
#         labels.extend(['endurance', 'cardiovascular', 'HIIT'])
#     elif fitness_goal == 'stress_relief' or fitness_goal == 'flexibility':
#         labels.extend(['mobility', 'therapy', 'mindfulness'])
#     if 'cardiovascular' not in labels and steps_count < 5000:
#         labels.append('cardiovascular')
#     if 'mobility' not in labels and 'mindfulness' not in labels and 'therapy' not in labels:
#         if stress_level > 0 or sleeping_hours < 5:
#             labels.extend(['mobility', 'mindfulness', 'therapy'])
#     return list(set(labels))

def assign_labels(fitness_goal, age, sleeping_hours, steps_count, fitness_level, stress_level):
    weights = {
        'cardiovascular': 1,
        'HIIT': 1,
        'strength': 1,
        'endurance': 1,
        'muscle_training': 1,
        'mobility': 1,
        'therapy': 1,
        'mindfulness': 1
    }

    labels = []

    if 'cardiovascular' not in labels and steps_count < 5000:
        weights.update({
            "cardiovascular" : weights['cardiovascular'] + 1
        })

    if stress_level > 0 or sleeping_hours < 5:
            weights.update({
                'mobility': weights['mobility'] + 1,
                'mindfulness': weights['mindfulness'] + 1,
                'therapy': weights['therapy'] + 1
            })
    if age > 50:
        weights.update({
                'cardiovascular': weights['cardiovascular'] - 1,
            })
    if fitness_goal == 'weight_loss':
        weights.update({
            'cardiovascular': weights['cardiovascular'] + 1,
            'HIIT': weights['HIIT'] + 1,
            'strength': weights['strength'] + 1,
            'endurance': weights['endurance'] + 1
        })
    elif fitness_goal == 'muscle_gain':
        weights.update({
            'strength': weights['strength'] + 1,
            'muscle_training': weights['muscle_training'] + 1
        })
    elif fitness_goal == 'endurance':
        weights.update({
            'endurance': weights['endurance'] + 1,
            'HIIT': weights['HIIT'] + 1,
            'cardiovascular': weights['cardiovascular'] + 1
        })
    elif fitness_goal in ['stress_relief', 'flexibility']:
        weights.update({
            'mindfulness': weights['mindfulness'] + 1,
            'therapy': weights['therapy'] + 1,
            'mobility': weights['mobility'] + 1
        })

    # Prioritize categories with higher weights
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    for category, weight in sorted_weights[:6]:
        if category not in labels:
            labels.append(category)

    return labels[:6]  # Ensure the length of labels is always 5


# Generate synthetic dataset
def generate_dataset(num_samples):
    data = []
    for _ in range(num_samples):
        fitness_goal = np.random.choice(fitness_goals)
        age = np.random.randint(age_range[0], age_range[1] + 1)
        sleeping_hours = np.random.uniform(sleeping_hours_range[0], sleeping_hours_range[1])

        if fitness_goal in ['weight_loss', 'muscle_gain']:
            steps_count = np.random.randint(10000, 20000)
            stress_level = np.random.randint(1, 2)
        elif fitness_goal == 'endurance':
            steps_count = np.random.randint(5000, 10000)
            stress_level = 1
        else:
            steps_count = np.random.randint(0, 5000)
            stress_level = np.random.randint(0, 1)

        fitness_level = np.random.randint(fitness_level_range[0], fitness_level_range[1] + 1)
        labels = assign_labels(fitness_goal, age, sleeping_hours, steps_count, fitness_level, stress_level)
        data.append([fitness_goal, age, sleeping_hours, steps_count, fitness_level, stress_level, labels])

    columns = ['fitness_goal', 'age', 'sleeping_hours', 'steps_count', 'fitness_level', 'stress_level', 'labels']
    df = pd.DataFrame(data, columns=columns)
    return df

# Preprocess data
def preprocess_data(df):
    label_encoder = LabelEncoder()
    ohe = OneHotEncoder(sparse_output=False)

    # Encode fitness_goal with LabelEncoder
    df['fitness_goal_encoded'] = label_encoder.fit_transform(df['fitness_goal'])

    # One-hot encode the fitness_goal
    fitness_goal_ohe = ohe.fit_transform(df[['fitness_goal_encoded']])
    fitness_goal_ohe_df = pd.DataFrame(fitness_goal_ohe,
                                      columns=[f"fitness_goal_{i}" for i in range(fitness_goal_ohe.shape[1])])

    # Drop the original and intermediate fitness_goal columns
    df = pd.concat([df.drop(['fitness_goal', 'fitness_goal_encoded'], axis=1), fitness_goal_ohe_df], axis=1)

    # Assuming 'labels' are lists, need to prepare them for One-hot encoding
    df['labels'] = df['labels'].apply(lambda x: ','.join(sorted(x)))
    labels_ohe = ohe.fit_transform(df[['labels']])

    labels_ohe_df = pd.DataFrame(labels_ohe,
                                 columns=[f"label_{i}" for i in range(labels_ohe.shape[1])])


    # Separate features and labels
    features = df.drop('labels', axis=1)
    labels = labels_ohe_df

    return features, labels, label_encoder, ohe

# Split the data
def split_data(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Train the model
def train_model(X_train, y_train):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(y_train.shape[1], activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy}")

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

    print(f"Dataset saved to {filename}")


def preprocess_input_data(input_df, label_encoder, features):
    ohe = OneHotEncoder(sparse_output=False)

    # Encode fitness_goal with LabelEncoder using the same encoder from training data
    input_df['fitness_goal_encoded'] = label_encoder.transform(input_df['fitness_goal'])

    # One-hot encode the fitness_goal
    fitness_goal_ohe = ohe.fit_transform(input_df[['fitness_goal_encoded']])
    fitness_goal_ohe_df = pd.DataFrame(fitness_goal_ohe,
                                      columns=[f"fitness_goal_{i}" for i in range(fitness_goal_ohe.shape[1])])

    # Drop the original and intermediate fitness_goal columns
    input_df = pd.concat([input_df.drop(['fitness_goal', 'fitness_goal_encoded'], axis=1), fitness_goal_ohe_df], axis=1)

    # Ensure that input data has the same number of features as the training data
    # Add dummy columns for missing features, if any
    missing_cols = set(features.columns) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0

    # Reorder columns to match the order of features in the training data
    input_features = input_df[features.columns]

    return input_features



def make_prediction():
    pass



# Main function
def run():
    path_to_save = os.path.join("datasets", "fitness-dataset.csv")
    file_exist = os.path.exists(path_to_save)
    if file_exist:
       df = pd.read_csv(path_to_save)
    else:
        df = generate_dataset(40000)
        save_to_csv(df, path_to_save)
    
    features, labels, label_encoder, ohe = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(features, labels)


    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    path_to_save_model = "models"
    model.save("models/aplha_model.keras")
    # tf.saved_model.save(model, "models")

    # input_data = {
    #   'fitness_goal': ['muscle_gain'],
    #   'age': [48],
    #   'sleeping_hours': [7.5],
    #   'steps_count': [19200],
    #   'fitness_level': [1],
    #   'stress_level': [1]
    # }
    # input_df = pd.DataFrame(input_data)

    # # # Preprocess input data
    # input_features = preprocess_input_data(input_df, label_encoder,features)

    # # # Make predictions
    # predictions = model.predict(input_features)
    # print(predictions.shape)


    # labels = []
    # for pred in zip(fitness_categories, predictions[0]):
    #     label, score = pred
    #     labels.append(label)


    # print("Predicted labels:", labels)


