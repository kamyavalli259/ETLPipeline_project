'''

import sys
import os
import pandas as pd




sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from src.clean import clean_dataframe
from src.clean import clean_users
from src.logger import logger

'''
'''
import os
import sys

#sys.path.append(os.path.abspath(".."))

# importing
from src.clean import clean_dataframe, clean_users
import pandas as pd
'''
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from src.clean import clean_dataframe, clean_users



'''
to test clean dataframe general cleaner going through removing duplicates, 
if it is working correctly 
'''


def test_clean_dataframe():

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

    


