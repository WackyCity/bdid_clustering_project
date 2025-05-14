import os
import pandas as pd

# Directory with CSV files
input_dir = "."

# Keys to filter files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# List of columns to sum
columns_to_sum = [
    "cp_level_y",
    #"cp_level_y.1",
    "cp_r_citing_zero_y",
    #"cp_r_citing_zero_y.1",
    "cp_r_citing_nonzero_y",
    #"cp_r_citing_nonzero_y.1"
    "tr_citing_y", 
    #"tr_citing_y.1", 
    "cp_r_cited_zero_y",
    #"cp_r_cited_zero_y.1",
    "cp_r_cited_nonzero_y", 
    #"cp_r_cited_nonzero_y.1", 
    "tr_cited_y",
    #"tr_cited_y.1"
]

print(f"{'Key':<10} {'File':<40}")
print('-' * 110)

for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            try:
                df = pd.read_csv(file_path)
                print(f"{key:<10} {filename:<40}")

                for col in columns_to_sum:
                    if col in df.columns:
                        col_sum = pd.to_numeric(df[col], errors='coerce').sum()
                        print(f"    {col:<30} {col_sum:>15.2f}")
                    else:
                        print(f"    {col:<30} {'[Column missing]':>15}")
            except Exception as e:
                print(f"{key:<10} {filename:<40} Error reading file: {e}")
