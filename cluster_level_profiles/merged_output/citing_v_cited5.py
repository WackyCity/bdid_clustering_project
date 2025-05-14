import os
import pandas as pd
import numpy as np

# === CONFIGURATION ===
input_dir = "."  # 🔁 Replace this with your actual path
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# === RESULTS CONTAINERS ===
summary_results = []
all_rows = []

for key in keys:
    for fname in os.listdir(input_dir):
        if key in fname and fname.endswith(".csv"):
            path = os.path.join(input_dir, fname)
            try:
                df = pd.read_csv(path)

                # Convert key columns to numeric
                citing_x = pd.to_numeric(df.get('tr_citing_x.1'), errors='coerce')
                cited_x = pd.to_numeric(df.get('tr_cited_x.1'), errors='coerce')
                citing_y = pd.to_numeric(df.get('tr_citing_y.1'), errors='coerce')
                cited_y = pd.to_numeric(df.get('tr_cited_y.1'), errors='coerce')

                # Prevent divide-by-zero
                cited_x = cited_x.replace(0, np.nan)
                cited_y = cited_y.replace(0, np.nan)

                # Compute percent differences
                percent_diff_net = (citing_x - cited_x) / cited_x
                percent_diff_clus = (citing_y - cited_y) / cited_y
                diff = percent_diff_clus - percent_diff_net

                # Label as more_citing or more_cited
                labels = diff.apply(
                    lambda x: 'more_citing' if pd.notna(x) and x > 0
                    else ('more_cited' if pd.notna(x) and x < 0 else 'neutral')
                )

                # Pull node count and edge density (assumed to be last 3 cols)
                node_count = pd.to_numeric(df.iloc[:, -3], errors='coerce')
                edge_density = pd.to_numeric(df.iloc[:, -1], errors='coerce')

                # Collect row-level data
                df_stats = pd.DataFrame({
                    'key': key,
                    'file': fname,
                    'label': labels,
                    'node_count': node_count,
                    'edge_density': edge_density,
                    'percent_difference_network_tr': percent_diff_net,
                    'percent_difference_cluster_tr': percent_diff_clus,
                    'difference': diff,
                    'tr_citing_x.1': citing_x,
                    'tr_cited_x.1': cited_x,
                    'tr_citing_y.1': citing_y,
                    'tr_cited_y.1': cited_y,
                })

                all_rows.append(df_stats)

                # Summary statistics by label
                def group_avg(label):
                    subset = df_stats[df_stats['label'] == label]
                    return {
                        'avg_node_count': subset['node_count'].mean(),
                        'avg_edge_density': subset['edge_density'].mean()
                    }

                stats_citing = group_avg('more_citing')
                stats_cited = group_avg('more_cited')
                stats_all = group_avg('more_citing')  # default
                stats_all['avg_node_count'] = df_stats['node_count'].mean()
                stats_all['avg_edge_density'] = df_stats['edge_density'].mean()

                summary_results.append({
                    'key': key,
                    'file': fname,
                    'total_clusters': len(df_stats),
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

# === CREATE SUMMARY DATAFRAME ===
summary_df = pd.DataFrame(summary_results)

# === SAVE SUMMARY CSV ===
summary_out = os.path.join(input_dir, "cluster_comparison_summary.csv")
summary_df.to_csv(summary_out, index=False)
print(f"\n📁 Summary CSV saved to: {summary_out}")

# === SAVE DETAILED ROW-LEVEL DATA ===
if all_rows:
    detailed_df = pd.concat(all_rows, ignore_index=True)
    detail_out = os.path.join(input_dir, "cluster_comparison_detailed.csv")
    detailed_df.to_csv(detail_out, index=False)
    print(f"📄 Detailed data CSV saved to: {detail_out}")

# === PRINT TABLE TO CONSOLE ===
if not summary_df.empty:
    cols = [
        'key', 'file', 'total_clusters', 'more_citing', 'more_cited',
        'avg_node_count_citing', 'avg_edge_density_citing',
        'avg_node_count_cited', 'avg_edge_density_cited',
        'avg_node_count_all', 'avg_edge_density_all'
    ]
    print("\n=== Cluster Comparison Summary ===")
    print(summary_df[cols].round(2).to_string(index=False))
else:
    print("❌ No valid data processed.")
