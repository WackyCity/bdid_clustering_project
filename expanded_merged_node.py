import os
import pandas as pd

# Use the current working directory
input_directory = '.'  # Current directory where the script is located
output_directory = '.'  # You can use the same directory or specify a different one

# List all CSV files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):  # Check if the file is a CSV
        file_path = os.path.join(input_directory, filename)  # Get full file path
        merged_df = pd.read_csv(file_path)  # Load the CSV into DataFrame
        
        # List of specified columns to calculate differences and percent drops
        columns_to_process = ['cp_level', 'cp_r_citing_zero', 'cp_r_citing_nonzero', 'tr_citing', 
                              'cp_r_cited_zero', 'cp_r_cited_nonzero', 'tr_cited']
        
        # Calculate differences and percent drops for the specified columns
        for column in columns_to_process:
            # Calculate the difference between the '_x' and '_y' columns for each specified column
            merged_df[f'{column}_diff'] = merged_df[f'{column}_x'] - merged_df[f'{column}_y']
            
            # Calculate the percent drop between the '_x' and '_y' columns
            merged_df[f'{column}_percent_drop'] = ((merged_df[f'{column}_y'] - merged_df[f'{column}_x']) / merged_df[f'{column}_x']) * 100
        
        # Calculate the differences and percent drops for the degree-related columns if they exist
        if 'network_degree' in merged_df.columns and 'cluster_degree' in merged_df.columns:
            merged_df['degree_diff'] = merged_df['network_degree'] - merged_df['cluster_degree']
            merged_df['degree_percent_drop'] = ((merged_df['cluster_degree'] - merged_df['network_degree']) / merged_df['network_degree']) * 100

        if 'network_indegree' in merged_df.columns and 'cluster_indegree' in merged_df.columns:
            merged_df['indegree_diff'] = merged_df['network_indegree'] - merged_df['cluster_indegree']
            merged_df['indegree_percent_drop'] = ((merged_df['cluster_indegree'] - merged_df['network_indegree']) / merged_df['network_indegree']) * 100

        if 'network_outdegree' in merged_df.columns and 'cluster_outdegree' in merged_df.columns:
            merged_df['outdegree_diff'] = merged_df['network_outdegree'] - merged_df['cluster_outdegree']
            merged_df['outdegree_percent_drop'] = ((merged_df['cluster_outdegree'] - merged_df['network_outdegree']) / merged_df['network_outdegree']) * 100

        # Create an output file name based on the input file name (e.g., 'data1.csv' -> 'expanded_data1.csv')
        output_file_name = f"expanded_{filename}"
        output_file_path = os.path.join(output_directory, output_file_name)
        
        # Export the modified DataFrame to the new CSV file
        merged_df.to_csv(output_file_path, index=False)

        print(f"Processed and exported: {output_file_path}")
