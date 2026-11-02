"""
Assignment 1: Predict the price of an Uber ride.

Steps performed:
    1. Pre-process the dataset.
    2. Identify outliers.
    3. Check the correlation.
    4. Train linear regression and random forest regression models and
       compare R2 / RMSE.

Dataset: Uber Fares Dataset (Kaggle)
https://www.kaggle.com/datasets/yasserh/uber-fares-dataset

Download `uber.csv` from the link above and place it next to this script
to use the real data. If it is not found, a synthetic dataset with the
same schema is generated so the pipeline still runs end to end.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_FILE = os.path.join(os.path.dirname(__file__), "uber.csv")


def load_data():
    if os.path.exists(DATA_FILE):
        print(f"Loading real dataset from {DATA_FILE}")
        return pd.read_csv(DATA_FILE)

    print(f"'{DATA_FILE}' not found - generating a synthetic sample dataset instead.")
    print("Download the real dataset from Kaggle and place it as 'uber.csv' for the actual assignment.\n")
    rng = np.random.default_rng(42)
    n = 2000
    pickup_lat = rng.uniform(40.70, 40.80, n)
    pickup_lon = rng.uniform(-74.02, -73.95, n)
    dropoff_lat = pickup_lat + rng.normal(0, 0.03, n)
    dropoff_lon = pickup_lon + rng.normal(0, 0.03, n)
    passenger_count = rng.integers(1, 5, n)

    df = pd.DataFrame({
        "key": range(n),
        "fare_amount": np.nan,  # filled below once distance is known
        "pickup_datetime": pd.date_range("2015-01-01", periods=n, freq="h"),
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
    })

    dist = haversine(df.pickup_latitude, df.pickup_longitude, df.dropoff_latitude, df.dropoff_longitude)
    df["fare_amount"] = 2.5 + 1.8 * dist + rng.normal(0, 1.5, n)
    # Inject a few outliers on purpose, to be caught by the IQR step.
    outlier_idx = rng.choice(n, size=10, replace=False)
    df.loc[outlier_idx, "fare_amount"] *= 15
    return df


def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def preprocess(df):
    df = df.dropna().copy()

    for col in ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]:
        df = df[df[col].between(-180, 180)]

    df["distance_km"] = haversine(
        df.pickup_latitude, df.pickup_longitude, df.dropoff_latitude, df.dropoff_longitude
    )
    df = df[(df.fare_amount > 0) & (df.distance_km > 0)]
    return df


def remove_outliers_iqr(df, column):
    q1, q3 = df[column].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = df[column].between(lower, upper)
    print(f"Outliers removed on '{column}': {(~mask).sum()} rows (bounds: [{lower:.2f}, {upper:.2f}])")
    return df[mask]


def plot_boxplots(df, title_suffix):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.boxplot(y=df["fare_amount"], ax=axes[0]).set_title(f"fare_amount ({title_suffix})")
    sns.boxplot(y=df["distance_km"], ax=axes[1]).set_title(f"distance_km ({title_suffix})")
    plt.tight_layout()
    plt.show()


def plot_correlation(corr_matrix):
    plt.figure(figsize=(5, 4))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation matrix")
    plt.show()


if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)

    print(f"\nDataset shape after cleaning: {df.shape}")

    plot_boxplots(df, "before")
    df = remove_outliers_iqr(df, "fare_amount")
    df = remove_outliers_iqr(df, "distance_km")
    plot_boxplots(df, "after")

    print("\nCorrelation with fare_amount:")
    corr_matrix = df[["fare_amount", "distance_km", "passenger_count"]].corr()
    corr = corr_matrix["fare_amount"].sort_values(ascending=False)
    print(corr)
    plot_correlation(corr_matrix)

    features = ["distance_km", "passenger_count"]
    X = df[features]
    y = df["fare_amount"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lr = LinearRegression().fit(X_train, y_train)
    rf = RandomForestRegressor(n_estimators=200, random_state=42).fit(X_train, y_train)

    print(f"\n{'Model':20} | {'R2':>8} | {'RMSE':>8}")
    print("-" * 42)
    for name, model in [("Linear Regression", lr), ("Random Forest", rf)]:
        preds = model.predict(X_test)
        r2 = r2_score(y_test, preds)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        print(f"{name:20} | {r2:>8.4f} | {rmse:>8.4f}")
