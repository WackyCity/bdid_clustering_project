import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import spearmanr

# Configuration
input_dir = "."  # 🔁 Replace this with your actual directory
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']
target_columns = [
    "cp_r_citing_zero_y", "cp_r_citing_nonzero_y",
    "cp_r_cited_zero_y", "cp_r_cited_nonzero_y",
    "tr_citing_y", "tr_cited_y"
]

output_dir = os.path.join(input_dir, "scatter_plots")
os.makedirs(output_dir, exist_ok=True)
pdf_path = os.path.join(output_dir, "scatter_edge_density_correlations.pdf")

# Hot pink for modularity, default colors for others
special_color = '#ff1493'
key_colors = {}

# Start PDF
with PdfPages(pdf_path) as pdf:
    for target_col in target_columns:
        plt.figure(figsize=(8, 6))
        all_rho = []

        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        color_index = 0
        background_key = '0.2'
        keys_ordered = [background_key] + [k for k in keys if k != background_key]

        for key in keys_ordered:
            for fname in os.listdir(input_dir):
                if key in fname and fname.endswith(".csv"):
                    path = os.path.join(input_dir, fname)
                    try:
                        df = pd.read_csv(path)

                        edge_density = pd.to_numeric(df.iloc[:, -1], errors='coerce')
                        target_vals = pd.to_numeric(df.get(target_col), errors='coerce')

                        valid = (~edge_density.isna()) & (~target_vals.isna())
                        edge_density = edge_density[valid]
                        target_vals = target_vals[valid]

                        if not edge_density.empty:
                            # Color selection
                            if key == "modularity":
                                color = special_color
                            else:
                                if key not in key_colors:
                                    key_colors[key] = color_cycle[color_index % len(color_cycle)]
                                    color_index += 1
                                color = key_colors[key]

                            # Background key gets lower alpha and zorder
                            is_background = key == background_key
                            plt.scatter(
                                edge_density,
                                target_vals,
                                label=key,
                                alpha=0.3 if is_background else 0.6,
                                s=15 if is_background else 25,
                                color=color,
                                zorder=0 if is_background else 1
                            )

                            rho, _ = spearmanr(edge_density, target_vals)
                            all_rho.append((key, rho))
                    except Exception as e:
                        print(f"[{key}] Failed on {fname}: {e}")

        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Edge Density (log)")
        plt.ylabel(f"{target_col} (log)")
        plt.title(f"Edge Density vs {target_col}")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend(title="Key", fontsize=8)

        if all_rho:
            cor_text = "\n".join([f"{k}: ρ = {r:.2f}" for k, r in all_rho if pd.notna(r)])
            plt.annotate(cor_text, xy=(0.05, 0.95), xycoords='axes fraction',
                         ha='left', va='top', fontsize=9,
                         bbox=dict(boxstyle="round", fc="w", ec="0.5"))

        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"\n✅ PDF with background plot for key '0.2' saved at:\n{pdf_path}")
