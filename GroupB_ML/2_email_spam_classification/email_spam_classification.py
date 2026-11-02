"""
Assignment 2: Email spam classification (binary classification) using
K-Nearest Neighbors and Support Vector Machine, with a performance
comparison.

Dataset: Email Spam Classification Dataset (Kaggle)
https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv

Download `emails.csv` from the link above and place it next to this
script to use the real data (word-count features + a 'Prediction'
column: 0 = Not Spam, 1 = Spam). If it is not found, a synthetic
dataset with the same shape is generated instead.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

DATA_FILE = os.path.join(os.path.dirname(__file__), "emails.csv")


def load_data():
    if os.path.exists(DATA_FILE):
        print(f"Loading real dataset from {DATA_FILE}")
        df = pd.read_csv(DATA_FILE)
        drop_cols = [c for c in df.columns if c.lower() in ("email no.", "email no", "id")]
        df = df.drop(columns=drop_cols, errors="ignore")
        return df

    print(f"'{DATA_FILE}' not found - generating a synthetic word-count dataset instead.")
    print("Download the real dataset from Kaggle and place it as 'emails.csv' for the actual assignment.\n")
    rng = np.random.default_rng(42)
    n_samples, n_words = 1000, 50
    labels = rng.integers(0, 2, n_samples)
    # Spam emails get higher counts for a "spammy" subset of words.
    word_counts = rng.poisson(lam=1.0, size=(n_samples, n_words))
    spam_word_idx = slice(0, 10)
    word_counts[labels == 1, spam_word_idx] += rng.poisson(lam=4.0, size=(labels.sum(), 10))

    columns = [f"word_{i}" for i in range(n_words)]
    df = pd.DataFrame(word_counts, columns=columns)
    df["Prediction"] = labels
    return df


if __name__ == "__main__":
    df = load_data()
    target_col = "Prediction" if "Prediction" in df.columns else df.columns[-1]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5).fit(X_train_scaled, y_train)
    svm = SVC(kernel="rbf", random_state=42).fit(X_train_scaled, y_train)

    print(f"{'Model':20} | {'Accuracy':>10}")
    print("-" * 34)
    for name, model in [("KNN", knn), ("SVM", svm)]:
        preds = model.predict(X_test_scaled)
        acc = accuracy_score(y_test, preds)
        print(f"{name:20} | {acc:>10.4f}")
        print(f"\n--- {name} classification report ---")
        print(classification_report(y_test, preds, target_names=["Not Spam", "Spam"]))
        print(f"Confusion matrix:\n{confusion_matrix(y_test, preds)}\n")

        ConfusionMatrixDisplay(
            confusion_matrix(y_test, preds), display_labels=["Not Spam", "Spam"]
        ).plot()
        plt.title(f"{name} - Confusion Matrix")
        plt.show()
