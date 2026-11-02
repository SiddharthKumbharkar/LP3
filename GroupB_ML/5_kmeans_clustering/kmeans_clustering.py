"""
Assignment 5: K-Means clustering on sales data, with the number of
clusters determined via the elbow method. A hierarchical clustering
comparison is included as well.

Dataset: Sample Sales Data Dataset (Kaggle)
https://www.kaggle.com/datasets/kyanyoga/sample-sales-data

Download `sales_data_sample.csv` from the link above (use encoding=
'latin1') and place it next to this script to use the real data. If it
is not found, a synthetic dataset with similar numeric fields is
generated instead.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA_FILE = os.path.join(os.path.dirname(__file__), "sales_data_sample.csv")
FEATURES = ["QUANTITYORDERED", "PRICEEACH", "SALES", "MSRP"]


def load_data():
    if os.path.exists(DATA_FILE):
        print(f"Loading real dataset from {DATA_FILE}")
        return pd.read_csv(DATA_FILE, encoding="latin1")

    print(f"'{DATA_FILE}' not found - generating a synthetic sales dataset instead.")
    print("Download the real dataset from Kaggle and place it as 'sales_data_sample.csv' for the actual assignment.\n")
    rng = np.random.default_rng(42)
    n = 1000
    cluster_centers = rng.uniform(20, 200, size=(4, len(FEATURES)))
    cluster_id = rng.integers(0, 4, n)
    data = cluster_centers[cluster_id] + rng.normal(0, 8, size=(n, len(FEATURES)))
    data = np.clip(data, 1, None)
    return pd.DataFrame(data, columns=FEATURES)


if __name__ == "__main__":
    df = load_data()
    available = [c for c in FEATURES if c in df.columns]
    df = df.dropna(subset=available)

    X = StandardScaler().fit_transform(df[available])

    print("Elbow method - inertia for k = 1..10:")
    inertias = []
    for k in range(1, 11):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        inertias.append(km.inertia_)
        print(f"  k={k:>2} -> inertia={km.inertia_:.2f}")

    plt.plot(range(1, 11), inertias, "o-")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia")
    plt.title("Elbow method")
    plt.show()

    # Simple automatic elbow pick: largest drop in inertia slope.
    diffs = np.diff(inertias)
    second_diffs = np.diff(diffs)
    best_k = int(np.argmax(second_diffs)) + 2  # offset for double-diff indexing
    best_k = max(2, min(best_k, 10))
    print(f"\nSelected number of clusters (elbow heuristic): k = {best_k}")

    kmeans = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(X)
    df["kmeans_cluster"] = kmeans.labels_
    print(f"\nK-Means cluster sizes:\n{df['kmeans_cluster'].value_counts().sort_index()}")

    if "SALES" in df.columns and "QUANTITYORDERED" in df.columns:
        plt.scatter(df["SALES"], df["QUANTITYORDERED"], c=df["kmeans_cluster"], cmap="viridis", s=15)
        plt.xlabel("SALES")
        plt.ylabel("QUANTITYORDERED")
        plt.title(f"K-Means clusters (k={best_k})")
        plt.show()
    else:
        plt.scatter(df[available[0]], df[available[1]], c=df["kmeans_cluster"], cmap="viridis", s=15)
        plt.xlabel(available[0])
        plt.ylabel(available[1])
        plt.title(f"K-Means clusters (k={best_k})")
        plt.show()

    linked = linkage(X, method="ward")
    hierarchical_labels = fcluster(linked, t=best_k, criterion="maxclust")
    df["hierarchical_cluster"] = hierarchical_labels
    print(f"\nHierarchical cluster sizes:\n{df['hierarchical_cluster'].value_counts().sort_index()}")

    plt.figure(figsize=(10, 4))
    dendrogram(linked, truncate_mode="lastp", p=30, show_leaf_counts=True)
    plt.title("Hierarchical clustering dendrogram (truncated)")
    plt.xlabel("Cluster size")
    plt.ylabel("Distance")
    plt.show()
