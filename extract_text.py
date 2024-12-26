import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Test the function
if __name__ == "__main__":
    pdf_path = "example_contract.pdf"  # Replace with your PDF file path
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text[:500])  # Print the first 500 characters

