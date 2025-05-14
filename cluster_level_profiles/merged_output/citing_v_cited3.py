import os
import pandas as pd

# === CONFIGURATION ===
input_dir = "."  # 🔁 Replace with actual path
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# === RESULTS CONTAINER ===
results = []

for key in keys:
    for fname in os.listdir(input_dir):
        if key in fname and fname.endswith(".csv"):
            path = os.path.join(input_dir, fname)
            try:
                df = pd.read_csv(path)

                # Ensure numeric conversion
                citing_x = pd.to_numeric(df.get('tr_citing_x.1'), errors='coerce')
                cited_x = pd.to_numeric(df.get('tr_cited_x.1'), errors='coerce')
                citing_y = pd.to_numeric(df.get('tr_citing_y.1'), errors='coerce')
                cited_y = pd.to_numeric(df.get('tr_cited_y.1'), errors='coerce')

                # Avoid divide-by-zero
                cited_x = cited_x.replace(0, pd.NA)
                cited_y = cited_y.replace(0, pd.NA)

                # Compute relative percent differences
                percent_diff_net = (citing_x - cited_x) / cited_x
                percent_diff_clus = (citing_y - cited_y) / cited_y
                diff = percent_diff_clus - percent_diff_net

                # Classify into more_citing / more_cited
                labels = diff.apply(lambda x: 'more_citing' if x > 0 else ('more_cited' if x < 0 else 'neutral'))

                # Node count and edge density are the last 3 columns
                node_count = pd.to_numeric(df.iloc[:, -3], errors='coerce')
                edge_density = pd.to_numeric(df.iloc[:, -1], errors='coerce')

                df_stats = pd.DataFrame({
                    'label': labels,
                    'node_count': node_count,
                    'edge_density': edge_density
                })

                def group_avg(label):
                    subset = df_stats[df_stats['label'] == label]
                    return {
                        'avg_node_count': subset['node_count'].mean(),
                        'avg_edge_density': subset['edge_density'].mean()
                    }

                stats_citing = group_avg('more_citing')
                stats_cited = group_avg('more_cited')
                stats_all = group_avg('all') if 'all' in df_stats['label'].values else {
                    'avg_node_count': df_stats['node_count'].mean(),
                    'avg_edge_density': df_stats['edge_density'].mean()
                }

                results.append({
                    'key': key,
                    'file': fname,
                    'total_clusters': len(df),
                    'more_citing': (labels == 'more_citing').sum(),
                    'more_cited': (labels == 'more_cited').sum(),
                    'avg_node_count_citing': stats_citing['avg_node_count'],
                    'avg_edge_density_citing': stats_citing['avg_edge_density'],
                    'avg_node_count_cited': stats_cited['avg_node_count'],
                    'avg_edge_density_cited': stats_cited['avg_edge_density'],
                    'avg_node_count_all': stats_all['avg_node_count'],
                    'avg_edge_density_all': stats_all['avg_edge_density']
                })

            except Exception as e:
                print(f"[{key}] Error reading {fname}: {e}")

# === DISPLAY AS TABLE ===
summary_df = pd.DataFrame(results)

# Debug: show actual column names
print("✅ Available columns in summary_df:", summary_df.columns.tolist())

# Expected output columns
cols = [
    'key', 'file', 'total_clusters', 'more_citing', 'more_cited',
    'avg_node_count_citing', 'avg_edge_density_citing',
    'avg_node_count_cited', 'avg_edge_density_cited',
    'avg_node_count_all', 'avg_edge_density_all'
]

# Safe access and print
if all(col in summary_df.columns for col in cols):
    print("\n=== Cluster Comparison Summary ===")
    print(summary_df[cols].round(2).to_string(index=False))
else:
    missing = [col for col in cols if col not in summary_df.columns]
    print(f"\n❌ Missing columns in results: {missing}")
