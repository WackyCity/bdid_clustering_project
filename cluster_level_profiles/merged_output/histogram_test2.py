import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Directory containing your CSV files
input_dir = "."
output_dir = os.path.join(input_dir, "column_histograms")
os.makedirs(output_dir, exist_ok=True)

# File keys to identify relevant CSVs
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# Columns to plot histograms for
columns_to_plot = [
    "cp_level_y.1",
    "cp_r_citing_zero_y.1", "cp_r_citing_zero_y.2", "cp_r_citing_zero_y.3",
    "cp_r_citing_nonzero_y", "cp_r_citing_nonzero_y.1", "cp_r_citing_nonzero_y.2", "cp_r_citing_nonzero_y.3",
    "tr_citing_y", "tr_citing_y.1", "tr_citing_y.2", "tr_citing_y.3",
    "cp_r_cited_zero_y", "cp_r_cited_zero_y.1", "cp_r_cited_zero_y.2", "cp_r_cited_zero_y.3",
    "cp_r_cited_nonzero_y", "cp_r_cited_nonzero_y.1", "cp_r_cited_nonzero_y.2", "cp_r_cited_nonzero_y.3",
    "tr_cited_y", "tr_cited_y.1"
]

# Prepare to collect data per column
column_data = {col: [] for col in columns_to_plot}
file_labels = {}

# Gather data from files
for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            try:
                df = pd.read_csv(file_path)
                label = key
                file_labels[label] = filename

                for col in columns_to_plot:
                    if col in df.columns:
                        values = pd.to_numeric(df[col], errors='coerce')
                        values = values[values > 0]  # Drop 0s and negatives for log scale
                        if not values.empty:
                            column_data[col].append((label, values))
            except Exception as e:
                print(f"[{key}] Error processing {filename}: {e}")

# Generate PDF with all histograms
pdf_path = os.path.join(output_dir, "all_histograms_logX.pdf")
with PdfPages(pdf_path) as pdf:
    for col, datasets in column_data.items():
        if not datasets:
            continue

        plt.figure(figsize=(10, 6))
        for label, values in datasets:
            plt.hist(values, bins=30, alpha=0.6, label=label, edgecolor='black')

        plt.xscale('log')  # ✅ Log-scale on x-axis
        plt.title(f"Histogram of {col} (Log X-axis)")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.legend(title="Key")
        plt.tight_layout()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        pdf.savefig()
        plt.close()

print(f"\n✅ Combined histogram PDF (with log-scaled x-axis) saved at:\n{pdf_path}")
