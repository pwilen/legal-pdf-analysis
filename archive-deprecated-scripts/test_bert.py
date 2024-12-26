from transformers import AutoTokenizer, AutoModel

try:
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
    model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

