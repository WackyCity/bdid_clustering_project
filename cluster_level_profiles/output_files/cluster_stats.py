import os
import pandas as pd

# Define the directory containing your CSV files
input_directory = '.'  # Replace with your input directory

# Create a dictionary to store aggregated statistics for each file
cluster_stats = {}

# List of columns we are interested in
columns_of_interest = [
    'cp_level_x', 'cp_r_citing_zero_x', 'cp_r_citing_nonzero_x', 'tr_citing_x', 
    'cp_r_cited_zero_x', 'cp_r_cited_nonzero_x', 'tr_cited_x',
    'cp_level_y', 'cp_r_citing_zero_y', 'cp_r_citing_nonzero_y', 'tr_citing_y', 
    'cp_r_cited_zero_y', 'cp_r_cited_nonzero_y', 'tr_cited_y',
    'network_degree', 'network_indegree', 'network_outdegree',
    'cluster_degree', 'cluster_indegree', 'cluster_outdegree'
]

# Iterate through the files in the directory (7 iterations)
for i in range(7):  # Repeat 7 times
    print(f"Iteration {i+1}:")
    
    # Iterate through all CSV files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):  # Check if the file is a CSV
            file_path = os.path.join(input_directory, filename)  # Full path to file
            
            # Load the CSV into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Check if 'Cluster_ID' and the required columns are present
            if 'Cluster_ID' in df.columns and all(col in df.columns for col in columns_of_interest):
                # Group by 'Cluster_ID' and calculate aggregate stats for the columns of interest
                grouped = df.groupby('Cluster_ID')[columns_of_interest].agg(
                    ['mean', 'sum', 'min', 'max'])  # You can add more aggregation functions as needed

                # Calculate the count of unique nodes in each cluster
                node_count = df.groupby('Cluster_ID')['node_id'].nunique()  # Count of unique node_id per Cluster_ID
                
                # Add the node_count to the aggregated statistics
                grouped['node_count'] = node_count

                # Store the result in the dictionary for this file and iteration
                if filename not in cluster_stats:
                    cluster_stats[filename] = {}

                # Store the aggregated stats for the current iteration
                cluster_stats[filename][f"Iteration {i+1}"] = grouped
    
    # After each iteration, print the aggregated statistics for each file
    print(f"Aggregated statistics after iteration {i+1}:")
    for filename, stats in cluster_stats.items():
        print(f"{filename} (Iteration {i+1}):")
        print(stats[f'Iteration {i+1}'].head())  # Show the first few rows as an example
    print()

# Optionally, save or process the results further (e.g., save to a CSV file)
# Example: Save aggregated stats for each file to a separate CSV
for filename, iterations in cluster_stats.items():
    for iteration, stats in iterations.items():
        output_file = f"{filename}_aggregated_{iteration}.csv"
        stats.to_csv(output_file)
        print(f"Saved aggregated stats for {filename} in {iteration} to {output_file}")
