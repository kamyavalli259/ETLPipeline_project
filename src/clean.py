import pandas as pd
from logger import logger

def clean_dataframe(dataframe):
    """
    Standardize and clean a pandas DataFrame.
    
    This function performs the following cleaning operations:
    - Creates a copy of the original DataFrame.
    - Standardizes column names by removing leading/trailing whitespace,
      converting names to lowercase, and replacing spaces with underscores.
    - Removes leading and trailing whitespace from string values.
    - Removes duplicate rows.
    - Replaces common missing-value placeholders
      ('', 'NA', 'N/A', 'NULL', 'null', 'None') with pandas NA values.
    
    Parameters:
    ----------
    dataframe : pandas.DataFrame
        The DataFrame to clean.
    
    Returns:
    -------
    pandas.DataFrame
        A cleaned DataFrame with standardized column names,
        trimmed string values, duplicates removed, and missing
        values normalized.
    """

    logger.info("Starting generic dataframe cleaning")
    cleaned = dataframe.copy()

    logger.debug("Standardizing column names")
    cleaned.columns = cleaned.columns.str.strip().str.lower().str.replace(" ", "_")

    logger.debug("Trimming whitespace from string columns")
    for column in cleaned.select_dtypes(include=['string', 'object']):
        cleaned[column] = cleaned[column].str.strip()

    before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    after = len(cleaned)
    logger.info(f"Removed {before - after} duplicate rows")
    cleaned = cleaned.replace(['', 'NA', 'N/A', 'NULL', 'null', 'None'], pd.NA)

    logger.info(
        f"Missing values after cleaning: {cleaned.isnull().sum().sum()}"
    )

    logger.info("Finished generic dataframe cleaning")

    return cleaned

def clean_users(dataframe):
    #logger.info("Cleaning users DataFrame.")
    users_cleaned = clean_dataframe(dataframe)

    logger.debug("Converting signup_date to datetime")
    users_cleaned['signup_date'] = pd.to_datetime(users_cleaned['signup_date'])

    logger.info(
        f"Users cleaned successfully. Rows: {len(users_cleaned)}"
    )
    return users_cleaned

def clean_sessions(dataframe):
    #logger.info("Cleaning sessions DataFrame.")
    sessions_cleaned = clean_dataframe(dataframe)

    logger.debug('Converting start_time to datetime')
    sessions_cleaned['start_time'] = pd.to_datetime(sessions_cleaned['start_time'])

    logger.info(
        f"Sessions cleaned successfully. Rows: {len(sessions_cleaned)}"
    )
    return sessions_cleaned

def clean_reviews(dataframe):
    """
    Total length is 1253
    purchase_id has 200 null values
    """
    #logger.info("Cleaning reviews DataFrame.")
    reviews_cleaned = clean_dataframe(dataframe)
    logger.debug('Converting review_date to datetime.')
    reviews_cleaned['review_date'] = pd.to_datetime(reviews_cleaned['review_date'])
    reviews_cleaned = reviews_cleaned.dropna()
    logger.info(f"Reviews cleaned succesfully. Rows: {len(reviews_cleaned)}")
    return reviews_cleaned

def clean_purchases(dataframe):
    #logger.info("Cleaning purchases DataFrame.")
    purchases_cleaned = clean_dataframe(dataframe)
    logger.debug('converting order_date to datetime.')
    purchases_cleaned['order_date'] = pd.to_datetime(purchases_cleaned['order_date'])
    logger.info(f'Purchases cleaned succesfully. Rows: {len(purchases_cleaned)}')
    return purchases_cleaned

def clean_products(dataframe):
    #logger.info("Cleaning Products DataFrame.")
    products_cleaned = clean_dataframe(dataframe)
    logger.debug('converting date_added to datetime')
    products_cleaned['date_added'] = pd.to_datetime(products_cleaned['date_added'])
    logger.info(f'Products cleaned succesfully. Rows: {len(products_cleaned)}')
    return products_cleaned

def clean_interactions(dataframe):
    #logger.info("Cleaning interactions DataFrame")
    interactions_cleaned = clean_dataframe(dataframe)
    logger.debug("converting timestamp to datetime")
    interactions_cleaned['timestamp'] = pd.to_datetime(interactions_cleaned['timestamp'])
    logger.info(f'Interactions cleaned succesfully. Rows: {len(interactions_cleaned)}')
    return interactions_cleaned

'''
call all the above functions
'''
'''
def main_clean(dataframes):
    functions = {'users': clean_users, 'sessions': clean_sessions, 'reviews': clean_reviews, 
                 'purchases': clean_purchases, 'products': clean_products, 'interactions': clean_interactions}
    cleaned_dataframes = {}
    for name in dataframes: 
        cleaned_dataframes[name] = functions[name](dataframes[name])
    return cleaned_dataframes
'''
