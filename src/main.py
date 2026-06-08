import readers.csv_reader as csvread
from pathlib import Path 

folder = Path('../data')
all_dataframes = []
for file in folder.iterdir():
    if file.is_file() and ".csv" in file.name:
        df = csvread.read_csv('../data/'+ file.name)
        all_dataframes.append(df)
print(all_dataframes)