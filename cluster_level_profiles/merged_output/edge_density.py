import os
import pandas as pd

# Set the directory where your 7 output CSVs are stored
output_dir = "."

# Use these keys to locate the 7 files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    files = [f for f in os.listdir(output_dir) if key in f and f.endswith('.csv')]
    if not files:
        print(f"[{key}] No file found.")
        continue

    file_path = os.path.join(output_dir, files[0])
    df = pd.read_csv(file_path)

    # Get the column names for node and edge count (assumed to be last two)
    node_col = df.columns[-2]
    edge_col = df.columns[-1]

    # Calculate edge density
    df['edge_density'] = df.apply(
        lambda row: row[edge_col] / (row[node_col] * (row[node_col] - 1) / 2)
        if pd.notnull(row[node_col]) and row[node_col] > 1 else 0,
        axis=1
    )

    # Save updated file (overwrite or change name)
    df.to_csv(file_path, index=False)
    print(f"[{key}] edge_density added to {file_path}")
