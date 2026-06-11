import pandas as pd
import os 


# Point to the data folder relative to where src/ lives
DATA_DIR = "../data"

# List all CSV files you want to load
files = [
    "interactions.csv"
]

def load_all_csvs(data_dir, files):
    datasets = {}
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"Loading {file_path}...")
        df = pd.read_csv(file_path)
        datasets[file.replace(".csv", "")] = df
    return datasets


def main():
    print("--- STARTING E-COMMERCE INGESTION WORKFLOW ---")
    
    datasets = load_all_csvs(DATA_DIR, files)
    
    
    for name, df in datasets.items():
        print(f"\nDataset: {name}")
        #print(df.head())
        print(df.info())
        print(df.isnull().sum())
        print(df.duplicated())
        print(df.columns)
        print(df.describe())
        categorical_columns = df.columns # Example list of columns
        for col in categorical_columns:
            #print(f"\nUnique values in {col}:")
            #print(df[col].unique())
            print(f"\nValue counts for {col}:")
            print(df[col].value_counts())
        
    
    print("--- INGESTION COMPLETE ---")

if __name__ == "__main__":
    main()
