import pandas as pd

input_csv = "validated_clauses_with_tones.csv"
data = pd.read_csv(input_csv)
print("Columns in the CSV:", data.columns)

