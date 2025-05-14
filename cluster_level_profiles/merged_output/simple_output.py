import os
import pandas as pd

# Directory containing your files
input_dir = "."

# Keys to identify matching files
keys = ['0.001', '0.005', '0.01', '0.05', '0.1', '0.2', 'modularity']

print(f"{'Key':<10} {'File':<40} {'Sum cp_level_y.1':>18}")
print('-' * 70)

for key in keys:
    for filename in os.listdir(input_dir):
        if key in filename and filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            try:
                df = pd.read_csv(file_path)

                if 'cp_level_y.1' in df.columns:
                    column_sum = pd.to_numeric(df['cp_level_y.1'], errors='coerce').sum()
                    print(f"{key:<10} {filename:<40} {column_sum:18.2f}")
                else:
                    print(f"{key:<10} {filename:<40} Column not found")
            except Exception as e:
                print(f"{key:<10} {filename:<40} Error: {e}")
