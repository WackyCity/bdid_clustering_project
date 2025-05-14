import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import spearmanr

# Configuration
input_dir = "."  # 🔁 Replace with your actual directory
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']
target_columns = [
    "cp_r_citing_zero_y",
    "cp_r_citing_nonzero_y",
    "cp_r_cited_zero_y",
    "cp_r_cited_nonzero_y"
]

output_dir = os.path.join(input_dir, "scatter_plots")
os.makedirs(output_dir, exist_ok=True)

pdf_path = os.path.join(output_dir, "scatter_edge_density_correlations.pdf")

# PDF for all plots
with PdfPages(pdf_path) as pdf:
    for target_col in target_columns:
        plt.figure(figsize=(8, 6))
        all_rho = []

        for key in keys:
            for fname in os.listdir(input_dir):
                if key in fname and fname.endswith(".csv"):
                    path = os.path.join(input_dir, fname)
                    try:
                        df = pd.read_csv(path)

                        # Assume edge_density is the last column
                        edge_density = pd.to_numeric(df.iloc[:, -1], errors='coerce')
                        target_vals = pd.to_numeric(df.get(target_col), errors='coerce')

                        # Drop rows with NaN
                        valid = (~edge_density.isna()) & (~target_vals.isna())
                        edge_density = edge_density[valid]
                        target_vals = target_vals[valid]

                        if not edge_density.empty:
                            plt.scatter(
                                edge_density,
                                target_vals,
                                label=key,
                                alpha=0.6,
                                s=20
                            )
                            # Spearman correlation
                            rho, _ = spearmanr(edge_density, target_vals)
                            all_rho.append((key, rho))

                    except Exception as e:
                        print(f"[{key}] Failed on {fname}: {e}")

        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Edge Density (log scale)")
        plt.ylabel(f"{target_col} (log scale)")
        plt.title(f"Edge Density vs {target_col}")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend(title="Key")

        # Annotate correlations
        if all_rho:
            cor_text = "\n".join([f"{k}: ρ = {r:.2f}" for k, r in all_rho if pd.notna(r)])
            plt.annotate(cor_text, xy=(0.05, 0.95), xycoords='axes fraction',
                         ha='left', va='top', fontsize=9, bbox=dict(boxstyle="round", fc="w", ec="0.5"))

        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"\n✅ Scatter plot PDF with correlations saved at:\n{pdf_path}")
