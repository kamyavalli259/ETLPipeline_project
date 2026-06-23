
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from src.clean import clean_dataframe, clean_users


def test_clean_dataframe():
    """Verify that clean_dataframe normalizes column names, trims whitespace, removes duplicates, and converts empty values to NaN.

    The test constructs a sample DataFrame with:
    - extra spaces in column names and string values
    - duplicate rows
    - an empty string in the Country column

    After calling clean_dataframe(), it asserts that:
    - column names are normalized to lowercase snake_case
    - leading/trailing spaces are removed from string values
    - duplicate rows are dropped
    - empty values are converted to missing values
    """

    df = pd.DataFrame({
        " User ID ": [1, 1, 2],
        " Name ": [" Alice ", " Alice ", "John"],
        "Country": ["USA", "USA", ""]
    })

    cleaned = clean_dataframe(df)

    # Column cleaned
    assert "user_id" in cleaned.columns

    # Whitespace removed
    assert cleaned["name"].iloc[0] == "Alice"

    #removing duplicates
    assert len(cleaned) == 2

    # Missing converted
    assert cleaned["country"].isna().sum() == 1

    


