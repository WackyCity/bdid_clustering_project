import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Directory containing your CSV files
input_dir = "."
output_dir = os.path.join(input_dir, "column_histograms")
os.makedirs(output_dir, exist_ok=True)

# Keys to match files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Columns to visualize
columns_to_plot = [
    "cp_level_y.1","cp_level_y", "cp_r_citing_zero_y.1",
    "cp_r_citing_nonzero_y", "cp_r_citing_nonzero_y.1",
    "tr_citing_y", "tr_citing_y.1", 
    "cp_r_cited_zero_y", "cp_r_cited_zero_y.1", 
    "cp_r_cited_nonzero_y", "cp_r_cited_nonzero_y.1", 
    "tr_cited_y", "tr_cited_y.1",
   "cp_level_x.1","cp_level_x", "cp_r_citing_zero_x.1",
    "cp_r_citing_nonzero_x", "cp_r_citing_nonzero_x.1",
    "tr_citing_x", "tr_citing_x.1", 
    "cp_r_cited_zero_x", "cp_r_cited_zero_x.1", 
    "cp_r_cited_nonzero_x", "cp_r_cited_nonzero_x.1", 
    "tr_cited_x", "tr_cited_x.1"
]

# Collect data for each column
column_data = {col: [] for col in columns_to_plot}

# Load and process CSVs
for key in keys:
    for fname in os.listdir(input_dir):
        if key in fname and fname.endswith('.csv'):
            path = os.path.join(input_dir, fname)
            try:
                df = pd.read_csv(path)
                for col in columns_to_plot:
                    if col in df.columns:
                        vals = pd.to_numeric(df[col], errors='coerce')
                        vals = vals[vals > 0]  # Log scale restriction
                        if not vals.empty:
                            column_data[col].append((key, vals))
            except Exception as e:
                print(f"Error reading {fname}: {e}")

# Create PDF of histograms
pdf_path = os.path.join(output_dir, "histograms_logXY_clean.pdf")
with PdfPages(pdf_path) as pdf:
    for col, datasets in column_data.items():
        if not datasets:
            continue

        plt.figure(figsize=(10, 6))
        for label, values in datasets:
            plt.hist(values, bins=30, histtype='step', label=label, linewidth=1.5)

        plt.xscale('log')
        plt.yscale('log')
        plt.title(f"Histogram of {col} (log-log, clean overlay)")
        plt.xlabel(col)
        plt.ylabel("Log Frequency")
        plt.legend(title="Key")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"\n✅ Saved all clean, log-log histograms to:\n{pdf_path}")
