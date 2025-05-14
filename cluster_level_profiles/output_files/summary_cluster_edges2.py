

import os
import pandas as pd
from collections import defaultdict

cluster_dir = "clusters/"
edge_dir = "cluster_edges_remaining/"
output_dir = "path/"  # Directory to save results
os.makedirs(output_dir, exist_ok=True)

keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

def read_file(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext == ".csv":
        return pd.read_csv(filepath)
    elif ext == ".tsv":
        return pd.read_csv(filepath, sep="\t")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_clusters(cluster_file):
    df = read_file(cluster_file)
    df.columns = df.columns[:2]  # Only first two columns
    df.columns = ['node', 'cluster']
    cluster_map = dict(zip(df['node'], df['cluster']))

    # Count number of nodes in each cluster
    node_counts = df['cluster'].value_counts().to_dict()
    
    return cluster_map, node_counts

def count_edges_per_cluster(edge_file, cluster_map):
    df = read_file(edge_file)
    df.columns = df.columns[:2]
    df.columns = ['u', 'v']
    
    edge_counts = defaultdict(int)

    for _, row in df.iterrows():
        u, v = row['u'], row['v']
        if u in cluster_map and v in cluster_map:
            cu, cv = cluster_map[u], cluster_map[v]
            if cu == cv:
                edge_counts[cu] += 1

    return edge_counts

# Main loop
for key in keys:
    cluster_files = [f for f in os.listdir(cluster_dir) if key in f and f.endswith(('.csv', '.tsv'))]
    edge_files = [f for f in os.listdir(edge_dir) if key in f and f.endswith(('.csv', '.tsv'))]

    if not cluster_files or not edge_files:
        print(f"[{key}] No matching files found.")
        continue

    cluster_file_path = os.path.join(cluster_dir, cluster_files[0])
    edge_file_path = os.path.join(edge_dir, edge_files[0])

    cluster_map, node_counts = load_clusters(cluster_file_path)
    edge_counts = count_edges_per_cluster(edge_file_path, cluster_map)

    # Merge cluster stats
    all_cluster_ids = set(node_counts.keys()) | set(edge_counts.keys())
    data = []
    for cid in sorted(all_cluster_ids):
        data.append({
            'cluster_id': cid,
            'nodes_in_cluster': node_counts.get(cid, 0),
            'intra_cluster_edges': edge_counts.get(cid, 0)
        })

    df_output = pd.DataFrame(data)
    output_path = os.path.join(output_dir, f"{key}_cluster_stats.csv")
    df_output.to_csv(output_path, index=False)

    print(f"[{key}] Output saved to {output_path}")
