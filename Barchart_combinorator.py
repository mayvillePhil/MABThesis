import os
import pandas as pd

# %%
def main():
# Define the base directory containing the folders
    base_dir = 'BarchartFutures/'
    combine_dir = base_dir + 'Combined data'
    # Define folders (e.g., Sept, May, Mar, July, Dec)
    folders = ['Sept', 'May', 'Mar', 'July', 'Dec']
    # %% md
    ## combine all the barchart data for the month contracts from 2004-2027
    # %%
    # Loop through each folder
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)

        # List all CSV files in the folder
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

        combined_data = pd.DataFrame()  # Empty DataFrame to store combined data

        # Loop through each CSV file
        for csv_file in csv_files:
            # Extract 'KEU05' (or similar) from the filename
            futures_contract_type = csv_file.split('_')[0].upper()

            # Load the CSV into a DataFrame
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path)

            # Add the 'Futures_Contract_Type' column at the beginning
            df.insert(0, 'Futures_Contract_Type', futures_contract_type)

            # Append to combined DataFrame
            combined_data = pd.concat([combined_data, df], ignore_index=True)

        # Save combined DataFrame for the folder
        combined_file_path = os.path.join(combine_dir, f'combined_{folder}.csv')
        combined_data.to_csv(combined_file_path, index=False)

        print(f"Combined CSV saved for {folder} at {combined_file_path}")

    # %% md
    ## combine all the data of the combined monthly contract
    # %%
    # Define the combined filenames for each month
    combined_files = [f'combined_{month}.csv' for month in ['Sept', 'May', 'Mar', 'July', 'Dec']]

    # Initialize an empty DataFrame for the final combined data
    final_combined_data = pd.DataFrame()

    # Loop through each combined file and append to final_combined_data
    for combined_file in combined_files:
        file_path = os.path.join(combine_dir, combined_file)

        # Check if the file exists (in case one of the months has no combined file)
        if os.path.exists(file_path):
            # Load the CSV into a DataFrame
            df = pd.read_csv(file_path)

            # Append to the final combined DataFrame
            final_combined_data = pd.concat([final_combined_data, df], ignore_index=True)
        else:
            print(f"File not found: {file_path}")

    # Save the final combined DataFrame to a new CSV
    final_combined_file_path = os.path.join(base_dir, 'final_combined.csv')
    final_combined_data.to_csv(final_combined_file_path, index=False)

    print(f"Final combined CSV saved at {final_combined_file_path}")
if __name__ == '__main__':
    main()