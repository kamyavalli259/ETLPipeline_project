
import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.readers.csv_reader import read_all_csvs
import pandas as pd



def test_read_all_csvs():

    """
    Test that read_all_csvs correctly loads all specified CSV files 
    and returns a dictionary of DataFrames.

    This function calls read_all_csvs with a list of expected file names 
    from the raw data directory. It verifies that:
    - The result is a dictionary.
    - The dictionary contains all expected dataset keys.
    - Each key maps to a pandas DataFrame.
    - The number of datasets loaded matches the number of files expected.

    The extraction function is expected to load each CSV file (e.g., users.csv, 
    products.csv, sessions.csv, interactions.csv, purchases.csv, reviews.csv) 
    and return a dictionary where each key corresponds to a file name (without extension) 
    and each value is a DataFrame of the file's data.
    
    This verifies 
    users.csv → users DataFrame
    products.csv → products DataFrame
    sessions.csv → sessions DataFrame
    interactions.csv → interactions DataFrame
    purchases.csv → purchases DataFrame
    reviews.csv → reviews DataFrame
    """

    files = [
        "users.csv",
        "products.csv",
        "sessions.csv",
        "interactions.csv",
        "purchases.csv",
        "reviews.csv"
    ]

    datasets = read_all_csvs("data", files)

    expected = [
        "users",
        "products",
        "sessions",
        "interactions",
        "purchases",
        "reviews"
    ]

    # Returns dictionary
    assert isinstance(datasets, dict)

    # Loaded all datasets
    assert len(datasets) == 6

    # Check expected keys exist
    for name in expected:
        assert name in datasets

    # Check each dataset is a DataFrame
    for df in datasets.values():
        assert isinstance(df, pd.DataFrame)