from readers.csv_reader import read_all_csvs
from clean import (
    clean_users,
    clean_products,
    clean_sessions,
    clean_interactions,
    clean_purchases,
    clean_reviews
)
import database
  
import pandas as pd
from logger import logger  # Import the logger
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
    try:
        logger.info("Starting the E-COMMERCE INGESTION WORKFLOW.")
        #print("--- STARTING E-COMMERCE INGESTION WORKFLOW ---")
        logger.debug("data from .csv")
        logger.info("Reading data from CSV files.")
        datasets = read_all_csvs(DATA_DIR, files)

        logger.info("Cleaning user data.")
        users_cleaned = clean_users(datasets['users'])

        logger.info("Cleaning product data.")
        products_cleaned = clean_products(datasets["products"])

        logger.info("Cleaning sessions data.")
        sessions_cleaned = clean_sessions(datasets["sessions"])

        logger.info("Cleaning interactions data.")
        interactions_cleaned = clean_interactions(datasets["interactions"])

        logger.info("Cleaning purchases data.")
        purchases_cleaned = clean_purchases(datasets["purchases"])

        logger.info("Cleaning reviews data.")
        reviews_cleaned = clean_reviews(datasets["reviews"])

        
        for name, df in datasets.items():
            print(f"\nDataset: {name}")
            print(df.head())
            print(df.info())
            print(df.columns)


        # Print a summary of each cleaned dataset
        print("\nCleaned Users Dataset:")
        print(users_cleaned.head())
        print(users_cleaned.info())
        print(users_cleaned.isnull().sum())
        
        print("\nCleaned Products Dataset:")
        print(products_cleaned.head())
        print(products_cleaned.info())
        
        print("\nCleaned Sessions Dataset:")
        print(sessions_cleaned.head())
        print(sessions_cleaned.info())
        
        print("\nCleaned Interactions Dataset:")
        print(interactions_cleaned.head())
        print(interactions_cleaned.info())
        
        print("\nCleaned Purchases Dataset:")
        print(purchases_cleaned.head())
        print(purchases_cleaned.info())
        
        print("\nCleaned Reviews Dataset:")
        print(reviews_cleaned.head())
        print(reviews_cleaned.info())

        
        # After cleaning, you can proceed to load data into the database or perform further analysis
        print("--- CLEANING COMPLETE ---")

        database.init_db()
        # After cleaning, insert data into PostgreSQL using database.py functions

        logger.info("Inserting users data into PostgreSQL.")
        database.insert_users_data(users_cleaned)

        logger.info("Inserting products data into PostgreSQL.")
        database.insert_products_data(products_cleaned)

        logger.info("Inserting sessions data into PostgreSQL.")
        database.insert_sessions_data(sessions_cleaned)

        logger.info("Inserting interactions data into PostgreSQL.")
        database.insert_interactions_data(interactions_cleaned)

        logger.info("Inserting purchases data into PostgreSQL.")
        database.insert_purchases_data(purchases_cleaned)

        logger.info("Inserting reviews data into PostgreSQL.")
        database.insert_reviews_data(reviews_cleaned)
        
        print("--- INGESTION COMPLETE ---")

    except Exception as e:
        logger.error(f"An error occurred during the ETL pipeline: {e}", exc_info=True)


        
        '''
        #Apply cleaning functions
        cleaned_datasets = main_clean(datasets)
        print('-----Accessing--users-----')
        print(cleaned_datasets['users'])
        print(type(cleaned_datasets['users']))

        # Print a summary of the cleaned data
        
        for name, df in cleaned_datasets.items():
            print(f"\nCleaned Dataset: {name}")
            print(df.head())
            print(df.info())
            for _, row in df.iterrows():
                print(row['user_id'])
        '''   

        #load and pass in the information
        

        

   
    
  

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



