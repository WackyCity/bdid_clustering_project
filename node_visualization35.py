import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

# === Config ===
edge_file = 'cit_hepph_cleaned.tsv'
target_node = 9606399

# === Cluster files ===
cluster_files = {
    "cpm_0.001": "cit_hepph_cpm_0.001.tsv",
    "cpm_0.005": "cit_hepph_cpm_0.005.tsv",
    "cpm_0.01":  "cit_hepph_cpm_0.01.tsv",
    "cpm_0.05":  "cit_hepph_cpm_0.05.tsv",
    "cpm_0.1":   "cit_hepph_cpm_0.1.tsv",
    "cpm_0.2":   "cit_hepph_cpm_0.2.tsv",
    "modularity": "cit_hepph_modularity.tsv"
}

# === Load edges ===
edges_df = pd.read_csv(edge_file, sep='\t', header=None, names=['source', 'target'])
G = nx.from_pandas_edgelist(edges_df, source='source', target='target', create_using=nx.DiGraph())

# === Visualization Function ===
def visualize_subgraph(cluster_file, label):
    clusters_df = pd.read_csv(cluster_file, sep='\t', header=None, names=['node', 'cluster'])
    clusters_df['node'] = clusters_df['node'].astype(int)
    node_cluster = dict(zip(clusters_df['node'], clusters_df['cluster']))
    subG = G.subgraph([n for n in G.nodes if n in node_cluster]).copy()

    if target_node not in subG:
        print(f"[!] Target node '{target_node}' not found in {label}. Skipping.")
        return

    # Neighbors
    level1_successors = set(subG.successors(target_node))
    level1_predecessors = set(subG.predecessors(target_node))
    nodes_to_include = {target_node} | level1_predecessors | level1_successors
    subgraph = subG.subgraph(nodes_to_include).copy()

    # Node appearance
    target_cluster = node_cluster[target_node]
    node_colors = []
    node_sizes = []

    for node in subgraph.nodes():
        if node == target_node:
            node_colors.append('red')
            node_sizes.append(100)
        elif node_cluster[node] == target_cluster:
            if node in level1_successors:
                node_colors.append('darkblue')  # Successor inside cluster (dark blue)
            else:
                node_colors.append('darkorange')  # Predecessor inside cluster (dark orange)
            node_sizes.append(60)
        else:
            if node in level1_successors:
                node_colors.append('lightblue')  # Successor outside cluster (light blue)
            else:
                node_colors.append('cyan')  # Predecessor outside cluster (cyan)
            node_sizes.append(60)

    # === Edge coloring logic ===
    edge_colors = []
    for u, v in subgraph.edges():
        if u == target_node and v in level1_successors:
            # Target -> Successor
            cited_successors = set(subG.successors(v))
            if any(succ in level1_successors for succ in cited_successors):
                edge_colors.append(mcolors.to_rgba('green', alpha=0.9))     # Green: Successor cites another successor
            else:
                edge_colors.append(mcolors.to_rgba('yellow', alpha=0.9))    # Yellow: Successor doesn't cite other successor

        elif v == target_node and u in level1_predecessors:
            # Target <- Predecessor
            cited_predecessors = set(subG.predecessors(u))
            if any(pred in level1_predecessors for pred in cited_predecessors):
                edge_colors.append(mcolors.to_rgba('darkorange', alpha=0.9))  # Dark Orange: Predecessor cites another predecessor
            else:
                edge_colors.append(mcolors.to_rgba('grey', alpha=0.9))  # Grey: Predecessor doesn't cite another predecessor

        # Ignore other edges for now (successor-successor, predecessor-predecessor)
        else:
            edge_colors.append(mcolors.to_rgba('lightcyan', alpha=0.5))     # Cyan for other edges, fallback

    # === Layout: spread center, ease outer ring ===
    pos = nx.spring_layout(subgraph, seed=42, k=2.5, iterations=100)
    for node in pos:
        if node_cluster[node] != target_cluster and node != target_node:
            pos[node] = [coord * 1.8 for coord in pos[node]]
        else:
            pos[node] = [coord * 0.9 for coord in pos[node]]

    # === Draw ===
    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors, arrows=True, arrowsize=12, width=0.8)
    plt.title(f"{label} – Target Node Neighborhood (Refined Colors)")
    plt.axis('off')
    plt.tight_layout()

    out_file = f"visual_{label}_target_view_shaded.png"
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Saved: {out_file}")

# === Run all files ===
for label, cluster_file in cluster_files.items():
    if not os.path.isfile(cluster_file):
        print(f"[!] File not found: {cluster_file}, skipping.")
        continue
    print(f"[+] Processing {cluster_file}")
    visualize_subgraph(cluster_file, label=label)
