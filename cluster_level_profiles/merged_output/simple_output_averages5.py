import os
import pandas as pd
from collections import defaultdict

# Directory with CSV files
input_dir = "."

# Keys to filter files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Columns to average
columns_to_average = [
    "cp_level_y",
    "cp_r_citing_zero_y",
    "cp_r_citing_nonzero_y",
    "tr_citing_y", 
    "cp_r_cited_zero_y",
    "cp_r_cited_nonzero_y", 
    "tr_cited_y",
]

# Header
print(f"{'Key':<10} {'Column':<30} {'Mean of Averages':>20}")
print('-' * 65)

# Store per-key column averages
key_column_averages = {key: defaultdict(list) for key in keys}

# Loop through files
for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            try:
                # Assumes header starts at row 4
                df = pd.read_csv(file_path, skiprows=3)
                for col in columns_to_average:
                    if col in df.columns:
                        avg = pd.to_numeric(df[col], errors='coerce').mean()
                        if pd.notnull(avg):
                            key_column_averages[key][col].append(avg)
            except Exception as e:
                print(f"{key:<10} {filename:<40} Error: {e}")

# Compute and print mean of averages
for key in keys:
    for col in columns_to_average:
        values = key_column_averages[key][col]
        if values:
            mean_of_avgs = sum(values) / len(values)
            print(f"{key:<10} {col:<30} {mean_of_avgs:>20.4f}")
        else:
            print(f"{key:<10} {col:<30} {'[No data]':>20}")
