import os
import pandas as pd
from extract_text import extract_text_from_pdf
from extract_clauses import extract_clauses
from process_tokens import process_text

# Define keywords for clauses
keywords = ["governing law", "termination", "liability", "confidentiality"]

def analyze_pdf(pdf_path):
    """Analyze a PDF to extract and process key clauses."""
    if not os.path.isfile(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return
    
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"Error: No text extracted from '{pdf_path}'.")
        return

    clauses = extract_clauses(text, keywords)
    if not clauses:
        print(f"No relevant clauses found in '{pdf_path}'.")
        return

    results = []
    for clause in clauses:
        embeddings = process_text(clause)
        results.append({"Clause": clause, "Embeddings Shape": embeddings.shape})

    # Display results in a table
    df = pd.DataFrame(results)
    print("\nExtracted Clauses and Embeddings:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze PDF files for key legal clauses.")
    parser.add_argument("pdf_path", help="Path to the PDF file to analyze.")
    args = parser.parse_args()

    analyze_pdf(args.pdf_path)

