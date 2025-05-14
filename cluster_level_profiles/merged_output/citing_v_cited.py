import os
import pandas as pd

# === CONFIG ===
input_dir = "."  # 🔁 Replace this with your actual path
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

# === RESULTS STORAGE ===
results = []

for key in keys:
    for fname in os.listdir(input_dir):
        if key in fname and fname.endswith(".csv"):
            path = os.path.join(input_dir, fname)
            try:
                df = pd.read_csv(path)

                # Convert relevant columns to numeric
                citing_x = pd.to_numeric(df.get('tr_citing_x.1'), errors='coerce')
                cited_x = pd.to_numeric(df.get('tr_cited_x.1'), errors='coerce')
                citing_y = pd.to_numeric(df.get('tr_citing_y.1'), errors='coerce')
                cited_y = pd.to_numeric(df.get('tr_cited_y.1'), errors='coerce')

                # Avoid divide-by-zero
                cited_x = cited_x.replace(0, pd.NA)
                cited_y = cited_y.replace(0, pd.NA)

                # Calculate percent differences relative to cited
                net_diff = (citing_x - cited_x) / cited_x
                clus_diff = (citing_y - cited_y) / cited_y
                overall_diff = clus_diff - net_diff

                # Classify rows
                more_citing = (overall_diff > 0).sum()
                more_cited = (overall_diff < 0).sum()

                results.append({
                    "key": key,
                    "file": fname,
                    "more_citing": more_citing,
                    "more_cited": more_cited
                })

            except Exception as e:
                print(f"[{key}] Error reading {fname}: {e}")

# === DISPLAY RESULTS ===
summary_df = pd.DataFrame(results)
print("\n=== Summary: More Citing vs More Cited (relative to cited_x/y.1) ===")
print(summary_df[["key", "file", "more_citing", "more_cited"]].to_string(index=False))
