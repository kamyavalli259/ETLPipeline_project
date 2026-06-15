import pandas as pd
import os 


def read_all_csvs(data_dir, files):
    """
    Load multiple CSV files into a dictionary of DataFrames.

    Parameters:
    - data_dir (str): The directory path where the CSV files are located.
    - files (list of str): A list of CSV file names to be loaded.

    Returns:
    - dict: A dictionary where each key is the file name (without the .csv extension) 
            and each value is a pandas DataFrame containing the data from that CSV file.
    """
    datasets = {}
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"Loading {file_path}...")
        df = pd.read_csv(file_path)
        datasets[file.replace(".csv", "")] = df
    return datasets
