import os
import pandas as pd

# --- CONFIGURATION ---
input_csv_dir = "output_files"
stats_dir = "."
output_dir = "merged_output"
os.makedirs(output_dir, exist_ok=True)

keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    input_files = [f for f in os.listdir(input_csv_dir) if key in f and f.endswith('.csv')]
    stats_files = [f for f in os.listdir(stats_dir) if key in f and f.endswith('.csv')]

    if not input_files or not stats_files:
        continue

    input_path = os.path.join(input_csv_dir, input_files[0])
    stats_path = os.path.join(stats_dir, stats_files[0])

    # Step 1: Read normally (row 0 = header)
    df_input = pd.read_csv(input_path, header=0, sep=None, engine='python')

    # Step 2: Manually read row 3 to get the correct name for the first column
    with open(input_path, 'r') as f:
        row3 = f.readlines()[2]  # row index 2 = 3rd line
    first_col_name = row3.split(',')[0].strip()

    # Step 3: Replace the first column's header
    df_input.columns = [first_col_name] + df_input.columns[1:].tolist()
    df_input.columns = df_input.columns.str.strip().str.lower()

    # Step 4: Ensure the first column is named 'cluster_id'
    if df_input.columns[0] != 'cluster_id':
        df_input.rename(columns={df_input.columns[0]: 'cluster_id'}, inplace=True)

    # Drop old counts if they exist
    df_input = df_input.drop(columns=[col for col in ['node_count', 'edge_count'] if col in df_input.columns])

    # Step 5: Read stats and normalize
    df_stats = pd.read_csv(stats_path, sep=None, engine='python')
    df_stats = df_stats.rename(columns={
        'Cluster_ID': 'cluster_id',
        'nodes_in_cluster': 'node_count',
        'intra_cluster_edges': 'edge_count'
    })
    df_stats.columns = df_stats.columns.str.strip().str.lower()

    # Step 6: Merge and save
    df_merged = df_input.merge(df_stats[['cluster_id', 'node_count', 'edge_count']], on='cluster_id', how='left')
    output_path = os.path.join(output_dir, input_files[0])
    df_merged.to_csv(output_path, index=False)
