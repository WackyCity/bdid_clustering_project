import os
import pandas as pd

# --- CONFIGURATION ---
input_csv_dir = "output_files"      # These have header on row 4 (skip first 3 rows)
stats_dir = "."         # Cluster stats (header is on row 1)
output_dir = "merged_output"      # Where to save updated files
os.makedirs(output_dir, exist_ok=True)

keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    input_files = [f for f in os.listdir(input_csv_dir) if key in f and f.endswith('.csv')]
    stats_files = [f for f in os.listdir(stats_dir) if key in f and f.endswith('.csv')]

    if not input_files or not stats_files:
        print(f"[{key}] No matching file in one or both directories.")
        continue

    input_path = os.path.join(input_csv_dir, input_files[0])
    stats_path = os.path.join(stats_dir, stats_files[0])

    # --- Read input file (skip first 3 rows) ---
    df_input = pd.read_csv(input_path, skiprows=3, sep=None, engine='python')

    # Trim columns with only NaN values
    df_input = df_input.dropna(axis=1, how='all')

    # Normalize column names
    df_input.columns = df_input.columns.str.strip().str.lower()

    # Explicitly rename potential cluster_id variants
    df_input = df_input.rename(columns={
        'clusterid': 'cluster_id',
        'cluster id': 'cluster_id',
        'cluster_id': 'cluster_id',
        'cluster_id ': 'cluster_id',  # handle extra spaces if present
    })

    # Debugging output to check column names
    print(f"[{key}] Input file columns: {df_input.columns.tolist()}")

    if 'cluster_id' not in df_input.columns:
        print(f"[{key}] 'cluster_id' missing in input file after processing: {input_files[0]}")
        continue

    # Drop old stats columns if they exist
    for col in ['node_count', 'edge_count']:
        if col in df_input.columns:
            df_input = df_input.drop(columns=col)

    # --- Read stats file normally (no skipping) ---
    df_stats = pd.read_csv(stats_path, sep=None, engine='python')
    df_stats.columns = df_stats.columns.str.strip()

    # Rename and normalize columns
    df_stats = df_stats.rename(columns={
        'Cluster_ID': 'cluster_id',
        'nodes_in_cluster': 'node_count',
        'intra_cluster_edges': 'edge_count'
    })
    df_stats.columns = df_stats.columns.str.strip().str.lower()

    if 'cluster_id' not in df_stats.columns:
        print(f"[{key}] 'cluster_id' missing in stats file after rename: {stats_files[0]}")
        continue

    # --- Merge ---
    df_merged = df_input.merge(df_stats, on='cluster_id', how='left')

    # --- Save ---
    output_path = os.path.join(output_dir, input_files[0])
    df_merged.to_csv(output_path, index=False)
    print(f"[{key}] Updated file saved to: {output_path}")
