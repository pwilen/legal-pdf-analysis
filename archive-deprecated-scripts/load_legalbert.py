from transformers import AutoTokenizer, AutoModel

# Load LEGAL-BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")

print("LEGAL-BERT model loaded successfully!")

