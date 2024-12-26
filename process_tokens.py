import torch
from transformers import AutoTokenizer, AutoModel

# Global variables initialized as None
_tokenizer = None
_model = None

def get_model():
    """Load and return the tokenizer and model as singletons."""
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
        _model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
    return _tokenizer, _model

def process_text(text):
    """Tokenize text and get embeddings from LEGAL-BERT."""
    tokenizer, model = get_model()
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state

# Test processing
if __name__ == "__main__":
    text = "This agreement is subject to the governing law of California."
    embeddings = process_text(text)
    print(f"Embeddings shape: {embeddings.shape}")  # Output: [batch_size, sequence_length, hidden_size]

