import pandas as pd
import os

# Folder where your files are stored
folder = "./clusters"  # Update if needed
edge_file = "cit_hepph_cleaned.tsv"  # Replace with your actual edge list file

# Load edge list (tab-separated, no header)
edges_df = pd.read_csv(os.path.join(folder, edge_file), sep='\t', header=None)
edges = list(zip(edges_df[0], edges_df[1]))

# Cluster keys you're interested in
valid_keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Find matching cluster files
cluster_files = [
    f for f in os.listdir(folder)
    if any(key in f for key in valid_keys)
]
cluster_files.sort(key=lambda x: valid_keys.index(next(k for k in valid_keys if k in x)))

# Process each cluster file
for cluster_file in cluster_files:
    try:
        # Read cluster file (no header, assign names)
        cluster_df = pd.read_csv(os.path.join(folder, cluster_file), sep='\t', header=None, names=['node', 'cluster'])

        # Map node to cluster
        cluster_map = dict(zip(cluster_df['node'], cluster_df['cluster']))

        # Classify edges
        inter, intra = 0, 0
        for u, v in edges:
            if cluster_map.get(u) != cluster_map.get(v):
                inter += 1
            else:
                intra += 1

        total = inter + intra
        inter_pct = inter / total * 100 if total else 0

        # Print stats
        print(f"\nCluster File: {cluster_file}")
        print(f"Total Edges: {total}")
        print(f"Intra-cluster Edges: {intra}")
        print(f"Inter-cluster Edges: {inter}")
        print(f"Percent Inter-cluster: {inter_pct:.2f}%")

    except Exception as e:
        print(f"⚠️ Error processing {cluster_file}: {e}")
