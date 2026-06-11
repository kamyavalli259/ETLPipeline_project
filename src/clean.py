import pandas as pd



def clean_dataframe(dataframe):
    """clean the dataset in the dataframe
    """
    cleaned = dataframe.copy()
    cleaned.columns = cleaned.columns.str.strip().str.lower().str.replace(" ", "_")
    for column in cleaned.select_dtypes(include=['string', 'object']):
        cleaned[column] = cleaned[column].str.strip()
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.replace(['', 'NA', 'N/A', 'NULL', 'null', 'None'], pd.NA)
    return cleaned


def clean_users(dataframe):
    users_cleaned = clean_dataframe(dataframe)
    users_cleaned['signup_date'] = pd.to_datetime(users_cleaned['signup_date'])
    return users_cleaned

def clean_sessions(dataframe):
    sessions_cleaned = clean_dataframe(dataframe)
    sessions_cleaned['start_time'] = pd.to_datetime(sessions_cleaned['start_time'])
    return sessions_cleaned


def clean_reviews(dataframe):
    """
    Total length is 1253
    purchase_id has 200 null values
    """
    reviews_cleaned = clean_dataframe(dataframe)
    reviews_cleaned['review_date'] = pd.to_datetime(reviews_cleaned['review_date'])
    reviews_cleaned = reviews_cleaned.dropna()
    return reviews_cleaned

def clean_purchases(dataframe):
    purchases_cleaned = clean_dataframe(dataframe)
    purchases_cleaned['order_date'] = pd.to_datetime(purchases_cleaned['order_date'])
    return purchases_cleaned

def clean_products(dataframe):
    products_cleaned = clean_dataframe(dataframe)
    products_cleaned['date_added'] = pd.to_datetime(products_cleaned['date_added'])
    return products_cleaned

def clean_interactions(dataframe):
    interactions_cleaned = clean_dataframe(dataframe)
    interactions_cleaned['timestamp'] = pd.to_datetime(interactions_cleaned['timestamp'])
    return interactions_cleaned


'''
call all the above functions
'''
def main_clean(dataframes):
    functions = {'users': clean_users, 'sessions': clean_sessions, 'reviews': clean_reviews, 
                 'purchases': clean_purchases, 'products': clean_products, 'interactions': clean_interactions}
    cleaned_dataframes = {}
    for name in dataframes: 
        cleaned_dataframes[name] = functions[name](dataframes[name])
    return cleaned_dataframes
    
