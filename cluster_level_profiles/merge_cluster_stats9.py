import pandas as pd
import os

# Directories
input_csv_dir = 'intercluster_outputs'  # Update as needed
stats_dir = 'output_files/former_without_intercluster'      # Update as needed
output_dir = 'new_aggregate_w_intercluster'

os.makedirs(output_dir, exist_ok=True)

# Clustering method keys
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

for key in keys:
    # Match files by key and .tsv extension
    input_files = [f for f in os.listdir(input_csv_dir) if key in f and f.endswith('.tsv')]
    stats_files = [f for f in os.listdir(stats_dir) if key in f and f.endswith('.tsv')]

    if not input_files or not stats_files:
        print(f"[{key}] Missing input or stats file.")
        continue

    input_path = os.path.join(input_csv_dir, input_files[0])
    stats_path = os.path.join(stats_dir, stats_files[0])

    # Step 1: Read input TSV with headers from row 0
    df_input = pd.read_csv(input_path, sep='\t', header=0)

    # Step 2: Get correct name for first column from row 3 (index 2)
    with open(input_path, 'r') as f:
        row3 = f.readlines()[2]
    first_col_name = row3.split('\t')[0].strip()

    # Step 3: Set the first column's name manually
    df_input.columns = [first_col_name] + df_input.columns[1:].tolist()
    df_input.columns = df_input.columns.str.strip().str.lower()

    # Step 4: Ensure 'cluster_id' is the first column name
    if df_input.columns[0] != 'cluster_id':
        df_input.rename(columns={df_input.columns[0]: 'cluster_id'}, inplace=True)

    # Step 5: Drop old count columns if present
    df_input = df_input.drop(columns=[col for col in ['node_count', 'edge_count'] if col in df_input.columns])

    # Step 6: Read and normalize the stats file (also TSV)
    df_stats = pd.read_csv(stats_path, sep='\t')
    df_stats = df_stats.rename(columns={
        'Cluster_ID': 'cluster_id',
        'nodes_in_cluster': 'node_count',
        'intra_cluster_edges': 'edge_count'
    })
    df_stats.columns = df_stats.columns.str.strip().str.lower()

    # Step 7: Coerce cluster_id to string for merging
    df_input['cluster_id'] = df_input['cluster_id'].astype(str)
    df_stats['cluster_id'] = df_stats['cluster_id'].astype(str)

    # Step 8: Merge and save result
    df_merged = df_input.merge(df_stats[['cluster_id', 'node_count', 'edge_count']], on='cluster_id', how='left')
    output_path = os.path.join(output_dir, input_files[0])
    df_merged.to_csv(output_path, sep='\t', index=False)

    print(f"[{key}] Merged and saved to {output_path}")
