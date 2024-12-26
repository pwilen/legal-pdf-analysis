def extract_clauses(text, keywords):
    """Extract clauses containing specific keywords."""
    clauses = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            clauses.append(keyword)
    return clauses

# Test clause extraction
if __name__ == "__main__":
    text = "This agreement is governed by the laws of California. Termination clauses are defined here."
    keywords = ["governing law", "termination"]
    clauses = extract_clauses(text, keywords)
    print("Extracted Clauses:", clauses)

