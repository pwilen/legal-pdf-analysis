import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

def load_embeddings(input_csv):
    """Load embeddings from a CSV file and process into numpy arrays."""
    print("Loading data from:", input_csv)
    data = pd.read_csv(input_csv)

    # Convert 'Embedding Shape' (string) into actual numpy arrays
    data["Embeddings"] = data["Embeddings"].apply(lambda x: np.array(eval(x), dtype=np.float32))
    
    # Check for valid embeddings
    data = data[data["Embeddings"].apply(lambda emb: len(emb) > 0)]
    return data

def compute_similarity_matrix(embeddings):
    """Compute cosine similarity matrix for embeddings."""
    if embeddings is None or len(embeddings) == 0:
        return None
    return cosine_similarity(embeddings)

def plot_similarity_heatmap(similarity_matrix, title, save_path=None):
    """Plot a heatmap for the similarity matrix."""
    if similarity_matrix is None:
        print(f"Skipping {title} due to missing data.")
        return

    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=False, cmap="coolwarm", square=True)
    plt.title(title)
    plt.xlabel("Clauses")
    plt.ylabel("Clauses")
    if save_path:
        plt.savefig(save_path)
        print(f"Heatmap saved to: {save_path}")
    plt.show()

def plot_embeddings_scatter(data, title, save_path=None):
    """Plot PCA visualization of embeddings."""
    embeddings = np.vstack(data["Embeddings"].values)
    tones = data["Tone"].values

    # Reduce dimensionality with PCA
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)

    plt.figure(figsize=(10, 8))
    for tone in set(tones):
        idx = tones == tone
        plt.scatter(reduced_embeddings[idx, 0], reduced_embeddings[idx, 1], label=tone, alpha=0.7)

    plt.title(title)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend()
    if save_path:
        plt.savefig(save_path)
        print(f"PCA scatter plot saved to: {save_path}")
    plt.show()

def main(input_csv):
    print("Processing embeddings and tones...")
    data = load_embeddings(input_csv)

    # Separate embeddings based on tone
    neutral_data = data[data["Tone"] == "neutral"]
    supplier_data = data[data["Tone"] == "supplier-friendly"]
    customer_data = data[data["Tone"] == "customer-friendly"]

    # Safely extract embeddings with checks
    neutral_embeddings = np.vstack(neutral_data["Embeddings"].values) if not neutral_data.empty else None
    supplier_embeddings = np.vstack(supplier_data["Embeddings"].values) if not supplier_data.empty else None
    customer_embeddings = np.vstack(customer_data["Embeddings"].values) if not customer_data.empty else None

    # Compute and plot similarity matrices
    print("Computing similarity matrices...")
    plot_similarity_heatmap(compute_similarity_matrix(neutral_embeddings), "Neutral Clauses Similarity Heatmap", save_path="outputs/visualizations/neutral_heatmap.png")
    plot_similarity_heatmap(compute_similarity_matrix(supplier_embeddings), "Supplier-Friendly Clauses Similarity Heatmap", save_path="outputs/visualizations/supplier_heatmap.png")
    plot_similarity_heatmap(compute_similarity_matrix(customer_embeddings), "Customer-Friendly Clauses Similarity Heatmap", save_path="outputs/visualizations/customer_heatmap.png")

    # Generate PCA scatter plot
    print("Generating PCA scatter plot...")
    if not data.empty:
        plot_embeddings_scatter(data, "PCA Visualization of Clause Embeddings", save_path="outputs/visualizations/embeddings_scatter.png")
    else:
        print("No data available for PCA scatter plot.")

if __name__ == "__main__":
    input_csv = "outputs/results/validated_clauses_with_tones.csv"  # Input CSV file
    main(input_csv)

