import os
import pandas as pd
import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModel
import torch
import torch.multiprocessing as mp

# Fix multiprocessing issue on macOS
if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)

# Initialize LEGAL-BERT tokenizer and model
def load_bert_model():
    """Load LEGAL-BERT model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
    model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
    return tokenizer, model

# Define keywords for clause extraction
keywords = ["confidentiality", "liability cap", "archiving", "data retention", "governing law", "payment terms"]

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def find_clauses(text, keywords):
    """Extract clauses containing specific keywords."""
    clauses = []
    for keyword in keywords:
        for line in text.split("\n"):
            if keyword.lower() in line.lower():
                clauses.append((keyword, line.strip()))
    return clauses

def process_text_with_bert(text, tokenizer, model):
    """Generate embeddings for text using LEGAL-BERT."""
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state.mean(dim=1)  # Mean pooling of embeddings

def analyze_contracts(base_folder, output_csv):
    """Analyze all contracts and extract relevant clauses."""
    results = []

    # Load model and tokenizer
    tokenizer, model = load_bert_model()

    # Walk through the folder structure
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                company_name = os.path.basename(root).replace("_", " ")
                contract_type = file.split("_")[0]

                print(f"Analyzing: {file_path}")
                text = extract_text_from_pdf(file_path)
                clauses = find_clauses(text, keywords)

                for keyword, clause in clauses:
                    # Process the clause with LEGAL-BERT
                    embeddings = process_text_with_bert(clause, tokenizer, model)
                    results.append({
                        "Company": company_name,
                        "Contract Type": contract_type,
                        "Clause": keyword,
                        "Content": clause,
                        "Embedding Shape": embeddings.shape
                    })

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    base_folder = "generated_contracts"  # Folder containing the test contracts
    output_csv = "outputs/results/contract_analysis_results.csv"
    analyze_contracts(base_folder, output_csv)

