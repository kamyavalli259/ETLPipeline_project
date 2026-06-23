import os
import sys
import pandas as pd

# Make src package importable from the tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.all import load_all_csvs


def test_load_all_csvs_reads_expected_files(tmp_path):
    """Verify that load_all_csvs loads CSV files into the expected DataFrame dictionary.

    This test creates temporary CSV files for products and reviews, then calls
    load_all_csvs() with that directory and file list. It asserts that:
    - the return value is a dictionary
    - keys are derived from filenames without the .csv extension
    - each value is a pandas DataFrame
    - loaded DataFrames contain the expected shape and sample values
    """

    product_csv = tmp_path / "products.csv"
    review_csv = tmp_path / "reviews.csv"

    pd.DataFrame(
        {
            "product_id": ["p1", "p2"],
            "product_name": ["Widget", "Gadget"],
            "price": [10.0, 15.5],
        }
    ).to_csv(product_csv, index=False)

    pd.DataFrame(
        {
            "review_id": ["r1", "r2"],
            "product_id": ["p1", "p2"],
            "rating": [5, 4],
        }
    ).to_csv(review_csv, index=False)

    datasets = load_all_csvs(str(tmp_path), ["products.csv", "reviews.csv"])

    assert isinstance(datasets, dict)
    assert set(datasets.keys()) == {"products", "reviews"}
    assert all(isinstance(df, pd.DataFrame) for df in datasets.values())

    assert datasets["products"].shape == (2, 3)
    assert datasets["reviews"].shape == (2, 3)
    assert datasets["products"].iloc[0]["product_name"] == "Widget"
    assert datasets["reviews"].iloc[1]["rating"] == 4
