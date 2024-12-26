import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

# Load LEGAL-BERT model and tokenizer
def load_bert_model():
    """Load LEGAL-BERT model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
    model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
    return tokenizer, model

def process_text_with_bert(text, tokenizer, model):
    """Generate embeddings for text using LEGAL-BERT."""
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state.mean(dim=1)  # Mean pooling of embeddings

def label_tone(content):
    """Assign tones to content based on keywords."""
    customer_keywords = ["highest level of care", "rigorous controls", "promptly reported"]
    supplier_keywords = ["reasonable efforts", "commercially reasonable", "not liable for"]

    content_lower = content.lower()
    if any(keyword in content_lower for keyword in customer_keywords):
        return "customer-friendly"
    elif any(keyword in content_lower for keyword in supplier_keywords):
        return "supplier-friendly"
    return "neutral"

def validate_embeddings(input_csv, output_csv):
    """Load clauses, process embeddings, label tones, and save results."""
    print(f"Loading data from: {input_csv}")
    data = pd.read_csv(input_csv)
    
    # Load LEGAL-BERT model and tokenizer
    print("Loading LEGAL-BERT model...")
    tokenizer, model = load_bert_model()

    # Process each clause
    results = []
    for _, row in data.iterrows():
        company = row["Company"]
        contract_type = row["Contract Type"]
        clause = row["Clause"]
        content = row["Content"]

        # Generate embeddings
        embedding = process_text_with_bert(content, tokenizer, model)
        embedding_list = embedding.squeeze(0).tolist()  # Convert tensor to list

        # Label tone
        tone = label_tone(content)

        # Append results
        results.append({
            "Company": company,
            "Contract Type": contract_type,
            "Clause": clause,
            "Content": content,
            "Embeddings": embedding_list,  # Save embeddings as list
            "Tone": tone
        })

    # Save results
    print("Saving results to CSV...")
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    print(f"Updated data saved to: {output_csv}")

if __name__ == "__main__":
    input_csv = "outputs/results/contract_analysis_results.csv"
    output_csv = "outputs/results/validated_clauses_with_tones.csv"
    validate_embeddings(input_csv, output_csv)

