# Legal Contract Analysis with LEGAL-BERT

This repository provides a comprehensive pipeline for analyzing legal contracts using **LEGAL-BERT embeddings**, tailored for **Contract Lifecycle Management 
(CLM)** applications. The project facilitates tasks such as clause classification, tone differentiation, metadata tagging, embedding validation, synthetic 
contract generation, and advanced visualization.

---

## Features

- **Clause Classification**: Categorizes clauses like confidentiality, payment terms, and scope of services.
- **Tone Differentiation**: Labels clauses as neutral, customer-friendly, or supplier-friendly.
- **Metadata Tagging**: Automates metadata extraction for CLM workflows.
- **Embedding Validation**: Validates LEGAL-BERT embeddings for tone and similarity metrics.
- **Synthetic Contract Generation**: Creates diverse, realistic contracts for robust testing.
- **Visualization Pipelines**: Includes heatmaps, PCA plots, ROC AUC, and Precision-Recall curves.

---

## Folder Structure

```plaintext
.
├── .git                     # Git repository folder
├── .gitignore               # Ignored files and directories
├── generated_contracts/     # Folder for synthetic contract outputs
├── outputs/                 # Folder for processed results and visualizations
├── example_contract.pdf     # Example PDF file for testing
├── active_scripts/
│   ├── analyze_contracts.py        # Main clause extraction and embedding script
│   ├── generate_random_contracts2.py # Generate synthetic contracts
│   ├── extract_text.py             # Text extraction from PDF files
│   ├── legal_pipeline.py           # Modular pipeline for legal analysis
│   ├── process_tokens.py           # Embedding generation using LEGAL-BERT
│   ├── validate_embeddings.py      # Embedding validation and tone assignment
│   ├── visualize_embeddings.py     # Heatmaps and PCA visualizations
│   ├── visualize_embeddings2.py    # Extended evaluation plots
└── README.md                # Project documentation
```

---

## Prerequisites

- Python 3.8 or higher
- Install dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd legal_pdf_analysis
   ```

2. **Set Up the Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

---

## Usage

### 1. Generate Synthetic Contracts

Create synthetic contracts for testing:

```bash
python active_scripts/generate_random_contracts2.py
```

### 2. Analyze Contracts

Extract clauses and generate embeddings:

```bash
python active_scripts/analyze_contracts.py
```

### 3. Validate Embeddings

Validate tone and similarity metrics:

```bash
python active_scripts/validate_embeddings.py
```

### 4. Visualize Results

Generate similarity heatmaps and evaluation plots:

```bash
python active_scripts/visualize_embeddings2.py
```
---
## Examples

### Generated Visualizations

The project produces the following visual outputs:

1. **Heatmaps**: Clause similarity matrices.
2. **PCA Plots**: Dimensionality reduction of embeddings.
3. **Evaluation Metrics**: ROC AUC and Precision-Recall curves.

---

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request for review.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgements

- **LEGAL-BERT**: [nlpaueb/legal-bert-base-uncased](https://huggingface.co/nlpaueb/legal-bert-base-uncased)
- **CUAD Dataset**: [CUAD](https://www.atticusprojectai.org/cuad) ##TO BE ADDED

---

## References

- [LEGAL-BERT Documentation](https://huggingface.co/nlpaueb/legal-bert-base-uncased)
- [CUAD Dataset Information](https://www.atticusprojectai.org/cuad)

