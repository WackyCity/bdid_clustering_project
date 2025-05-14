import os
import pandas as pd
import numpy as np

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

                # Convert necessary columns to numeric
                citing_x = pd.to_numeric(df.get('tr_citing_x.1'), errors='coerce')
                cited_x = pd.to_numeric(df.get('tr_cited_x.1'), errors='coerce')
                citing_y = pd.to_numeric(df.get('tr_citing_y.1'), errors='coerce')
                cited_y = pd.to_numeric(df.get('tr_cited_y.1'), errors='coerce')

                # Avoid divide-by-zero with np.nan
                cited_x = cited_x.replace(0, np.nan)
                cited_y = cited_y.replace(0, np.nan)

                # Compute percent differences
                percent_diff_net = (citing_x - cited_x) / cited_x
                percent_diff_clus = (citing_y - cited_y) / cited_y
                diff = percent_diff_clus - percent_diff_net

                # Handle nulls before comparison
                labels = diff.apply(
                    lambda x: 'more_citing' if pd.notna(x) and x > 0
                    else ('more_cited' if pd.notna(x) and x < 0
                          else 'neutral')
                )

                # Node count and edge density = last 3 columns
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
                stats_all = {
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

cols = [
    'key', 'file', 'total_clusters', 'more_citing', 'more_cited',
    'avg_node_count_citing', 'avg_edge_density_citing',
    'avg_node_count_cited', 'avg_edge_density_cited',
    'avg_node_count_all', 'avg_edge_density_all'
]

if not summary_df.empty and all(col in summary_df.columns for col in cols):
    print("\n=== Cluster Comparison Summary ===")
    print(summary_df[cols].round(2).to_string(index=False))
else:
    print("❌ No data to display or missing columns.")
# === SAVE TO CSV ===
output_path = os.path.join(input_dir, "cluster_comparison_summary.csv")
summary_df.to_csv(output_path, index=False)
print(f"\n📁 Summary CSV saved to: {output_path}")
