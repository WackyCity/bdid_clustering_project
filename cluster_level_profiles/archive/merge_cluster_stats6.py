import os
import pandas as pd

# --- CONFIGURATION ---
input_csv_dir = "output_files"       # Replace with your actual input directory
stats_dir = "."          # Replace with your actual stats output directory
output_dir = "merged_output"       # Replace with where you want merged files saved
os.makedirs(output_dir, exist_ok=True)

keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    input_files = [f for f in os.listdir(input_csv_dir) if key in f and f.endswith('.csv')]
    stats_files = [f for f in os.listdir(stats_dir) if key in f and f.endswith('.csv')]

    if not input_files or not stats_files:
        continue

    input_path = os.path.join(input_csv_dir, input_files[0])
    stats_path = os.path.join(stats_dir, stats_files[0])

    # Read input CSV, skipping first 3 rows to reach actual header (row 4)
    df_input = pd.read_csv(input_path, skiprows=2, sep=None, engine='python')
    df_input = df_input.dropna(axis=1, how='all')  # Remove empty columns

    # Force first column to be cluster_id
    df_input.columns = ['cluster_id'] + df_input.columns[1:].tolist()
    df_input.columns = df_input.columns.str.strip().str.lower()

    # Drop old counts if they exist
    df_input = df_input.drop(columns=[col for col in ['node_count', 'edge_count'] if col in df_input.columns])

    # Read stats CSV
    df_stats = pd.read_csv(stats_path, sep=None, engine='python')
    df_stats = df_stats.rename(columns={
        'Cluster_ID': 'cluster_id',
        'nodes_in_cluster': 'node_count',
        'intra_cluster_edges': 'edge_count'
    })
    df_stats.columns = df_stats.columns.str.strip().str.lower()

    # Merge
    df_merged = df_input.merge(df_stats[['cluster_id', 'node_count', 'edge_count']], on='cluster_id', how='left')

    # Save
    output_path = os.path.join(output_dir, input_files[0])
    df_merged.to_csv(output_path, index=False)
