import os
import pandas as pd
from collections import defaultdict

# Define directories
cluster_dir = "clusters/"
edge_dir = "cluster_edges_remaining/"
output_dir = "path/"  # Directory to save results
os.makedirs(output_dir, exist_ok=True)

# Keys to filter files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

def read_file(file_path):
    """ Read a TSV file (tab-separated values) """
    return pd.read_csv(file_path, sep='\t', header=None)  # No header as your file does not have headers

def load_clusters(cluster_file_path):
    """ Load cluster file and return a mapping from node to cluster """
    df = read_file(cluster_file_path)
    print("Columns in the cluster file:", df.columns)  # Print column names to inspect
    
    # Manually set column names as 'node' and 'cluster'
    df.columns = ['node', 'cluster']
    
    # Ensure 'node' column exists
    if 'node' not in df.columns:
        print(f"Error: 'node' column not found in {cluster_file_path}")
        return {}, {}  # Return empty dictionaries if 'node' column is missing

    cluster_map = df.set_index('node')['cluster'].to_dict()
    
    # Count number of nodes in each cluster
    node_counts = df['cluster'].value_counts().to_dict()
    
    return cluster_map, node_counts

def count_edges_per_cluster(edge_file, cluster_map):
    """ Count both intracluster and intercluster edges """
    df = read_file(edge_file)
    df.columns = df.columns[:2]  # Ensure that columns are 'u' and 'v' for the nodes
    df.columns = ['u', 'v']
    
    edge_counts_intra = defaultdict(int)  # Intra-cluster edges
    edge_counts_inter = defaultdict(int)  # Inter-cluster edges

    for _, row in df.iterrows():
        u, v = row['u'], row['v']
        if u in cluster_map and v in cluster_map:
            cu, cv = cluster_map[u], cluster_map[v]
            
            # Intracluster edge
            if cu == cv:
                edge_counts_intra[cu] += 1
            else:
                # Intercluster edge, increment for both clusters
                edge_counts_inter[cu] += 1
                edge_counts_inter[cv] += 1

    return edge_counts_intra, edge_counts_inter

# Main loop to process files
for key in keys:
    cluster_files = [f for f in os.listdir(cluster_dir) if key in f and f.endswith(('.csv', '.tsv'))]
    edge_files = [f for f in os.listdir(edge_dir) if key in f and f.endswith(('.csv', '.tsv'))]

    if not cluster_files or not edge_files:
        print(f"[{key}] No matching files found.")
        continue

    # Select the first matching cluster and edge file
    cluster_file_path = os.path.join(cluster_dir, cluster_files[0])
    edge_file_path = os.path.join(edge_dir, edge_files[0])

    # Load cluster data and edge counts
    cluster_map, node_counts = load_clusters(cluster_file_path)
    if not cluster_map:  # Skip if cluster map is empty due to error
        continue
    edge_counts_intra, edge_counts_inter = count_edges_per_cluster(edge_file_path, cluster_map)

    # Merge cluster stats
    all_cluster_ids = set(node_counts.keys()) | set(edge_counts_intra.keys()) | set(edge_counts_inter.keys())
    data = []
    for cid in sorted(all_cluster_ids):
        data.append({
            'cluster_id': cid,
            'nodes_in_cluster': node_counts.get(cid, 0),
            'intra_cluster_edges': edge_counts_intra.get(cid, 0),
            'inter_cluster_edges': edge_counts_inter.get(cid, 0)
        })

    # Convert data to a DataFrame and save to CSV
    df_output = pd.DataFrame(data)
    output_path = os.path.join(output_dir, f"{key}_cluster_stats.csv")
    df_output.to_csv(output_path, index=False)

    print(f"[{key}] Output saved to {output_path}")
