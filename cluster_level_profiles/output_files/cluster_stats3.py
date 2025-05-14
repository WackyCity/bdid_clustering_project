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

# Iterate through all CSV files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):  # Check if the file is a CSV
        file_path = os.path.join(input_directory, filename)  # Full path to file
        
        # Load the CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Print the columns to see if 'node_id' exists in the DataFrame
        print(f"Columns in {filename}: {df.columns.tolist()}")  # Print column names for debugging
        
        # Check if 'Cluster_ID' and the required columns are present
        if 'Cluster_ID' in df.columns and all(col in df.columns for col in columns_of_interest):
            # Group by 'Cluster_ID' and calculate aggregate stats for the columns of interest
            grouped = df.groupby('Cluster_ID')[columns_of_interest].agg(
                ['mean', 'sum', 'min', 'max'])  # You can add more aggregation functions as needed
            
            # Check if 'node_id' column exists before calculating node count
            if 'node_id' in df.columns:
                # Calculate the count of unique nodes in each cluster
                node_count = df.groupby('Cluster_ID')['node_id'].nunique()  # Count of unique node_id per Cluster_ID
                grouped['node_count'] = node_count
            else:
                print(f"'node_id' column not found in {filename}. Skipping node count aggregation.")
                grouped['node_count'] = None  # Add a placeholder or skip the node count
            
            # Edge Calculation based on cluster degree
            if 'cluster_degree' in df.columns:
                # For each cluster, sum the cluster_degree and divide by 2 to get the number of edges
                edge_count = df.groupby('Cluster_ID')['cluster_degree'].sum() / 2
                grouped['edge_count'] = edge_count
            else:
                print(f"'cluster_degree' column not found in {filename}. Skipping edge count aggregation.")
                grouped['edge_count'] = None  # Add a placeholder if no cluster_degree data

            # Store the result in the dictionary for this file
            cluster_stats[filename] = grouped
        
        else:
            print(f"Required columns missing in {filename}. Skipping this file.")
    
# After processing, print the aggregated statistics for each file
for filename, stats in cluster_stats.items():
    print(f"Aggregated statistics for {filename}:")
    print(stats.head())  # Show the first few rows as an example

    # Optionally, save the aggregated stats to a new CSV
    output_file = f"{filename}_aggregated.csv"
    stats.to_csv(output_file)
    print(f"Saved aggregated stats for {filename} to {output_file}")
