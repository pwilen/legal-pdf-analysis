import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve
from sklearn.metrics.pairwise import cosine_similarity

# Load embeddings and tones from CSV
def load_embeddings(file_path):
    print(f"Loading data from: {file_path}")
    data = pd.read_csv(file_path)
    data["Embeddings"] = data["Embeddings"].apply(lambda x: np.array(eval(x), dtype=np.float32))
    return data

# Compute similarity matrix for embeddings
def compute_similarity_matrix(embeddings):
    if len(embeddings) == 0:
        return np.array([[]])
    return cosine_similarity(np.vstack(embeddings))

# Generate and save heatmap
def generate_heatmap(similarity_matrix, labels, title, file_name):
    if similarity_matrix.size == 0:
        print(f"Skipping heatmap generation for {title} due to empty similarity matrix.")
        return
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, xticklabels=labels, yticklabels=labels, cmap="coolwarm", annot=False)
    plt.title(title)
    plt.xlabel("Clauses")
    plt.ylabel("Clauses")
    plt.tight_layout()
    plt.savefig(file_name)
    print(f"Heatmap saved to {file_name}")
    plt.close()

# Prepare evaluation data
def prepare_evaluation_data(data, similarity_matrix, tone_label):
    filtered_data = data[data["Tone"] == tone_label]
    indices = np.array(filtered_data.index)
    
    # Map indices to valid range for similarity matrix
    valid_indices = indices[indices < similarity_matrix.shape[0]]

    # Extract positives
    positive_scores = similarity_matrix[np.ix_(valid_indices, valid_indices)].flatten()
    positive_labels = np.ones_like(positive_scores)

    # Extract negatives
    all_indices = set(range(similarity_matrix.shape[0]))
    unrelated_indices = np.array(list(all_indices - set(valid_indices)))

    if len(unrelated_indices) == 0:
        negative_scores = np.array([])
        negative_labels = np.array([])
    else:
        num_negatives = min(len(unrelated_indices), len(positive_scores))
        sampled_negatives = np.random.choice(unrelated_indices, num_negatives, replace=False)
        negative_scores = similarity_matrix[np.ix_(valid_indices, sampled_negatives)].flatten()
        negative_labels = np.zeros_like(negative_scores)

    # Combine positive and negative samples
    scores = np.concatenate([positive_scores, negative_scores])
    labels = np.concatenate([positive_labels, negative_labels])

    return labels, scores

# Plot ROC AUC
def plot_roc_auc(labels, scores, tone_label, output_file):
    if len(set(labels)) < 2:
        print(f"Skipping ROC AUC plot for {tone_label} due to single-class labels.")
        return

    fpr, tpr, _ = roc_curve(labels, scores)
    roc_auc = roc_auc_score(labels, scores)

    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC curve (area = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"Receiver Operating Characteristic - {tone_label}")
    plt.legend(loc="lower right")
    plt.savefig(output_file)
    print(f"ROC AUC plot saved to {output_file}")
    plt.close()

# Plot Precision-Recall Curve
def plot_precision_recall(labels, scores, tone_label, output_file):
    if len(set(labels)) < 2:
        print(f"Skipping Precision-Recall plot for {tone_label} due to single-class labels.")
        return

    precision, recall, _ = precision_recall_curve(labels, scores)

    plt.figure()
    plt.plot(recall, precision, label=f"Precision-Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"Precision-Recall Curve - {tone_label}")
    plt.legend(loc="lower left")
    plt.savefig(output_file)
    print(f"Precision-Recall plot saved to {output_file}")
    plt.close()

# Main function to process and visualize embeddings
def main(input_csv):
    data = load_embeddings(input_csv)

    # Compute similarity matrices
    print("Computing similarity matrices...")
    neutral_embeddings = data[data["Tone"] == "neutral"]["Embeddings"].values
    supplier_embeddings = data[data["Tone"] == "supplier-friendly"]["Embeddings"].values

    neutral_similarity = compute_similarity_matrix(neutral_embeddings)
    supplier_similarity = compute_similarity_matrix(supplier_embeddings)

    # Generate heatmaps
    print("Generating heatmaps...")
    generate_heatmap(neutral_similarity, data[data["Tone"] == "neutral"]["Clause"].values, "Neutral Clauses Similarity", "outputs/visualizations/neutral_heatmap.png")
    generate_heatmap(supplier_similarity, data[data["Tone"] == "supplier-friendly"]["Clause"].values, "Supplier-Friendly Clauses Similarity", 
"outputs/visualizations/supplier_heatmap.png")

    # Generate ROC AUC and Precision-Recall plots
    print("Generating ROC AUC and Precision-Recall plots...")
    for tone_label, similarity_matrix in zip(["neutral", "supplier-friendly"], [neutral_similarity, supplier_similarity]):
        labels, scores = prepare_evaluation_data(data, similarity_matrix, tone_label)
        plot_roc_auc(labels, scores, tone_label, f"outputs/visualizations/roc_auc_{tone_label}.png")
        plot_precision_recall(labels, scores, tone_label, f"outputs/visualizations/precision_recall_{tone_label}.png")

if __name__ == "__main__":
    input_csv = "outputs/results/validated_clauses_with_tones.csv"
    main(input_csv)

