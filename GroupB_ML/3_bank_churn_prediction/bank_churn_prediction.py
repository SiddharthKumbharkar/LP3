"""
Assignment 3: Bank customer churn prediction using a neural network.

Steps performed:
    1. Read the dataset.
    2. Distinguish the feature and target set; split into train/test.
    3. Normalize the train and test data.
    4. Initialize and build the model.
    5. Print the accuracy score and confusion matrix.

Dataset: Churn Modelling Dataset (Kaggle)
https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling

Download `Churn_Modelling.csv` from the link above and place it next to
this script to use the real data. If it is not found, a synthetic
dataset with the same schema is generated instead.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_FILE = os.path.join(os.path.dirname(__file__), "Churn_Modelling.csv")
tf.random.set_seed(42)


def load_data():
    if os.path.exists(DATA_FILE):
        print(f"Loading real dataset from {DATA_FILE}")
        return pd.read_csv(DATA_FILE)

    print(f"'{DATA_FILE}' not found - generating a synthetic dataset instead.")
    print("Download the real dataset from Kaggle and place it as 'Churn_Modelling.csv' for the actual assignment.\n")
    rng = np.random.default_rng(42)
    n = 3000
    geography = rng.choice(["France", "Germany", "Spain"], n)
    gender = rng.choice(["Male", "Female"], n)
    age = rng.integers(18, 80, n)
    balance = rng.uniform(0, 200000, n)
    credit_score = rng.integers(350, 850, n)
    is_active = rng.integers(0, 2, n)

    churn_score = (
        (age > 50).astype(int) * 0.4
        + (balance < 20000).astype(int) * 0.3
        + (is_active == 0).astype(int) * 0.3
        + rng.normal(0, 0.2, n)
    )
    exited = (churn_score > 0.5).astype(int)

    return pd.DataFrame({
        "RowNumber": range(n),
        "CustomerId": range(100000, 100000 + n),
        "Surname": ["Sample"] * n,
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": rng.integers(0, 11, n),
        "Balance": balance,
        "NumOfProducts": rng.integers(1, 5, n),
        "HasCrCard": rng.integers(0, 2, n),
        "IsActiveMember": is_active,
        "EstimatedSalary": rng.uniform(10000, 150000, n),
        "Exited": exited,
    })


if __name__ == "__main__":
    df = load_data()

    drop_cols = [c for c in ["RowNumber", "CustomerId", "Surname"] if c in df.columns]
    df = df.drop(columns=drop_cols)

    df = pd.get_dummies(df, columns=["Geography", "Gender"], drop_first=True)

    X = df.drop(columns=["Exited"])
    y = df["Exited"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=0)

    plt.plot(history.history["accuracy"], label="train accuracy")
    plt.plot(history.history["val_accuracy"], label="val accuracy")
    plt.xlabel("epoch")
    plt.ylabel("accuracy")
    plt.legend()
    plt.title("Training history")
    plt.show()

    y_pred = (model.predict(X_test, verbose=0) > 0.5).astype(int).ravel()

    print(f"\nAccuracy score: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Confusion matrix:\n{confusion_matrix(y_test, y_pred)}")

    ConfusionMatrixDisplay(
        confusion_matrix(y_test, y_pred), display_labels=["Stayed", "Exited"]
    ).plot()
    plt.title("Confusion Matrix")
    plt.show()
