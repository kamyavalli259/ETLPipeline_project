from readers.csv_reader import load_all_csvs
from clean import main_clean  
import pandas as pd
import os 


# Point to the data folder relative to where src/ lives
DATA_DIR = "../data"

# List all CSV files you want to load
files = [
    "users.csv",
    "products.csv",
    "sessions.csv",
    "interactions.csv",
    "purchases.csv",
    "reviews.csv"
]


def main():
    print("--- STARTING E-COMMERCE INGESTION WORKFLOW ---")
    
    datasets = load_all_csvs(DATA_DIR, files)

    
    for name, df in datasets.items():
        print(f"\nDataset: {name}")
        print(df.head())
        print(df.info())
        print(df.columns)


    #Apply cleaning functions
    cleaned_datasets = main_clean(datasets)

    # Print a summary of the cleaned data
    for name, df in cleaned_datasets.items():
        print(f"\nCleaned Dataset: {name}")
        print(df.head())
        print(df.info())
    
    
    print("--- INGESTION COMPLETE ---")

if __name__ == "__main__":
    main()


'''
from pathlib import Path 

folder = Path('../data')
all_dataframes = []
for file in folder.iterdir():
    if file.is_file() and ".csv" in file.name:
        df = csvread.read_csv('../data/'+ file.name)
        all_dataframes.append(df)
print(all_dataframes)
'''



