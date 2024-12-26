from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")

def tokenize_text(text):
    """Tokenize the text for LEGAL-BERT."""
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    return tokens

# Test tokenization
if __name__ == "__main__":
    text = "This agreement is subject to the governing law of California."
    tokens = tokenize_text(text)
    print(tokens)

