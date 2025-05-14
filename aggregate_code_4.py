import pandas as pd
import os

def load_and_aggregate_spreadsheets(files):
    # Initialize an empty DataFrame to aggregate the data into
    aggregated_data = None

    for file in files:
        # Check if the file exists
        if not os.path.exists(file):
            print(f"Warning: '{file}' does not exist, skipping.")
            continue
        
        # Dynamically determine the file type based on file extension
        if file.endswith('.tsv'):
            sep = '\t'  # For TSV files, use tab as separator
        elif file.endswith('.csv'):
            sep = ','  # For CSV files, use comma as separator
        else:
            print(f"Warning: '{file}' is not a recognized file type (.csv or .tsv), skipping.")
            continue
        
        # Load the spreadsheet into a DataFrame
        df = pd.read_csv(file, sep=sep)

        # Use the first column as the 'Node_ID' column
        df.rename(columns={df.columns[0]: 'Node_ID'}, inplace=True)

        # Remove duplicate rows based on 'Node_ID'
        df = df.drop_duplicates(subset='Node_ID')

        # If this is the first file, initialize the aggregated data with it
        if aggregated_data is None:
            aggregated_data = df
        else:
            # Add suffixes to distinguish the columns from different files
            suffix = f"_{file.split('.')[0]}"  # Use file name (excluding extension) as suffix
            aggregated_data = pd.merge(aggregated_data, df, on='Node_ID', how='outer', suffixes=('', suffix))

        # Print shape of DataFrame before and after merging for debugging
        print(f"After merging file {file}, data shape is: {aggregated_data.shape}")
    
    return aggregated_data

# List of your files to aggregate
files = [
    'cit_hepph_cleaned.tsv', 
    'bdid_clustered-cit_hepph_cpm_0.001.csv', 
    'bdid-cit_hepph_cpm_0.001.csv', 
    'cit_hepph_cpm_0.001.tsv',
    'degstats-cit_hepph_cleaned-cit_hepph_cpm_0.001.csv', 
    'bdid_clustered-cit_hepph_cpm_0.01.csv', 
    'bdid-cit_hepph_cpm_0.01.csv', 
    'cit_hepph_cpm_0.01.tsv',
    'degstats-cit_hepph_cleaned-cit_hepph_cpm_0.01.csv', 
    'bdid_clustered-cit_hepph_cpm_0.1.csv', 
    'bdid-cit_hepph_cpm_0.1.csv', 
    'cit_hepph_cpm_0.1.tsv',
    'degstats-cit_hepph_cleaned-cit_hepph_cpm_0.1.csv', 
    'bdid_clustered-cit_hepph_modularity.csv', 
    'bdid-cit_hepph_modularity.csv', 
    'cit_hepph_modularity.tsv',
    'degstats-cit_hepph_cleaned-cit_hepph_modularity.csv'
]

# Aggregate the data from the files
aggregated_df = load_and_aggregate_spreadsheets(files)

# Check the aggregated data
if aggregated_df is not None:
    print(f"Aggregated data shape: {aggregated_df.shape}")
    print(aggregated_df.head())

    # Save the aggregated DataFrame to a new TSV file
    aggregated_df.to_csv('aggregated_statistics.tsv', sep='\t', index=False)
else:
    print("No files were successfully loaded or aggregated.")
