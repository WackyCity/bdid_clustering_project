import os
import pandas as pd
from collections import defaultdict
import numpy as np

# Directory with CSV files
input_dir = "."

# Keys to filter files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Columns to analyze
columns_to_analyze = [
    "cp_level_y",
    "cp_r_citing_zero_y",
    "cp_r_citing_nonzero_y",
    "tr_citing_y", 
    "cp_r_cited_zero_y",
    "cp_r_cited_nonzero_y", 
    "tr_cited_y",
]

# Print header
print(f"{'Key':<10} {'Column':<30} {'Mean':>10} {'Median':>10} {'Min':>10} {'Max':>10} {'Q1':>10} {'Q3':>10}")
print('-' * 100)

# Store per-key and per-column means
key_column_averages = {key: defaultdict(list) for key in keys}

# Process each file
for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            try:
                df = pd.read_csv(file_path, skiprows=3)  # Skip first 3 rows
                for col in columns_to_analyze:
                    if col in df.columns:
                        col_mean = pd.to_numeric(df[col], errors='coerce').mean()
                        if pd.notnull(col_mean):
                            key_column_averages[key][col].append(col_mean)
            except Exception as e:
                print(f"{key:<10} {filename:<40} Error reading file: {e}")

# Calculate and print summary statistics
for key in keys:
    for col in columns_to_analyze:
        values = key_column_averages[key][col]
        if values:
            arr = np.array(values)
            mean_val = arr.mean()
            median_val = np.median(arr)
            min_val = arr.min()
            max_val = arr.max()
            q1 = np.percentile(arr, 25)
            q3 = np.percentile(arr, 75)

            print(f"{key:<10} {col:<30} {mean_val:10.4f} {median_val:10.4f} {min_val:10.4f} {max_val:10.4f} {q1:10.4f} {q3:10.4f}")
        else:
            print(f"{key:<10} {col:<30} {'[No data]':>70}")
