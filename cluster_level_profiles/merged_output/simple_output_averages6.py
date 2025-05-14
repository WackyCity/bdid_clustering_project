import os
import pandas as pd

# Directory with CSV files
input_dir = "."

# Keys to filter files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Columns to sum
columns_to_sum = [
    "cp_level_y",
    "cp_r_citing_zero_y",
    "cp_r_citing_nonzero_y",
    "tr_citing_y", 
    "cp_r_cited_zero_y",
    "cp_r_cited_nonzero_y", 
    "tr_cited_y",
]

print(f"{'Key':<10} {'File':<40}")
print('-' * 110)

for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            try:
                # Skip first 3 rows; assumes data starts at row 4
                df = pd.read_csv(file_path, skiprows=3)

                # Total number of data rows
                num_rows = len(df)

                print(f"{key:<10} {filename:<40}")

                for col in columns_to_sum:
                    if col in df.columns:
                        col_sum = pd.to_numeric(df[col], errors='coerce').sum()
                        if num_rows > 0:
                            mean_val = col_sum / num_rows
                            print(f"    {col:<30} {mean_val:>15.4f}")
                        else:
                            print(f"    {col:<30} {'[No data rows]':>15}")
                    else:
                        print(f"    {col:<30} {'[Column missing]':>15}")
            except Exception as e:
                print(f"{key:<10} {filename:<40} Error reading file: {e}")
