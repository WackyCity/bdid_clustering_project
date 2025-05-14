import os
import pandas as pd

# --- CONFIGURATION ---
input_csv_dir = "."      # Original files to update
stats_dir = "output_files"         # New stats from cluster analysis
output_dir = "merged_output"      # Where to save updated files
os.makedirs(output_dir, exist_ok=True)

# Filenames should contain these keys to match corresponding files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    # --- Locate input and stats files ---
    input_files = [f for f in os.listdir(input_csv_dir) if key in f and f.endswith('.csv')]
    stats_files = [f for f in os.listdir(stats_dir) if key in f and f.endswith('.csv')]

    if not input_files or not stats_files:
        print(f"[{key}] No matching file in one or both directories.")
        continue

    input_path = os.path.join(input_csv_dir, input_files[0])
    stats_path = os.path.join(stats_dir, stats_files[0])

    # --- Read input file and normalize headers ---
    df_input = pd.read_csv(input_path, sep=None, engine='python')  # auto-detects comma/tab
    df_input.columns = df_input.columns.str.strip().str.lower()
    df_input = df_input.rename(columns={'clusterid': 'cluster_id'})

    if 'cluster_id' not in df_input.columns:
        print(f"[{key}] 'cluster_id' missing in input file: {input_files[0]}")
        continue

    # Drop old stats if present
    for col in ['node_count', 'edge_count']:
        if col in df_input.columns:
            df_input = df_input.drop(columns=col)

    # --- Read stats file and normalize headers ---
    df_stats = pd.read_csv(stats_path, sep=None, engine='python')
    df_stats.columns = df_stats.columns.str.strip().str.lower()
    df_stats = df_stats.rename(columns={
        'clusterid': 'cluster_id',
        'nodes_in_cluster': 'node_count',
        'intra_cluster_edges': 'edge_count'
    })

    if 'cluster_id' not in df_stats.columns:
        print(f"[{key}] 'cluster_id' missing in stats file: {stats_files[0]}")
        continue

    # --- Merge on cluster_id ---
    df_merged = df_input.merge(df_stats, on='cluster_id', how='left')

    # --- Save updated file ---
    output_path = os.path.join(output_dir, input_files[0])
    df_merged.to_csv(output_path, index=False)
    print(f"[{key}] Updated file saved to: {output_path}")
