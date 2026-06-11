import pandas as pd
import os 




def load_all_csvs(data_dir, files):
    datasets = {}
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"Loading {file_path}...")
        df = pd.read_csv(file_path)
        datasets[file.replace(".csv", "")] = df
    return datasets
