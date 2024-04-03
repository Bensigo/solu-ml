from dotenv import load_dotenv
from  ml import alpha
import tensorflow as tf
import pandas as pd
import os 


load_dotenv()



def main():
    print("start server ......")
    # alpha.run()
    model = tf.keras.models.load_model("./models/aplha_model.keras")

    path_to_save = os.path.join("datasets", "fitness-dataset.csv")
    df = pd.read_csv(path_to_save)
    features, labels, label_encoder, ohe = alpha.preprocess_data(df)

    input_data = {
      'fitness_goal': ['stress_relief'],
      'age': [48],
      'sleeping_hours': [4.5],
      'steps_count': [3000],
      'fitness_level': [1],
      'stress_level': [1]
    }
    input_df = pd.DataFrame(input_data)

    input_features = alpha.preprocess_input_data(input_df, label_encoder,features)

    predictions = model.predict(input_features)


    labels = []
    for pred in zip(alpha.fitness_categories, predictions[0]):
        label, score = pred
        print(f"{label}: {score}")
        labels.append(label)

    print("Predicted labels:", labels)

    


if __name__ == '__main__':
    main()