import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
from .logger import logger
import json
from pathlib import Path

def connect():
    """Create a PostgreSQL database connection using environment variables.

    The function loads environment variables from a `.env` file located next to
    `database.py`, then connects using `psycopg2.connect()`.

    Returns:
        psycopg2.extensions.connection: An open PostgreSQL connection.
    """
    env_path = Path(__file__).resolve().with_name(".env")
    load_dotenv(env_path)
    load_dotenv()
    conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DATABASE'),
    user=os.getenv('USER'), 
    password=os.getenv('PASSWORD'),  
    port=os.getenv('PORT') 
    )
    return conn

def init_db():
    """Initialize the PostgreSQL database schema for the ETL pipeline.

    This function connects to the database, drops any existing pipeline tables,
    and recreates the required tables for users, products, purchases, reviews,
    sessions, interactions, and staging rejects.
    """
    conn = connect()
    try:
        '''
        The with conn block ensures that if all operations inside it succeed, the transaction
        is committed automatically when the block ends.
        If any exception occurs inside the block, the transaction is rolled back automatically,
        so don't have to manually call conn.rollback()
        with conn: pattern is a clean way to handle transactions because it guarantees that 
        the commit or rollback happens based on whether the operations succeed or fail.
        '''
        with conn:
            with conn.cursor() as cursor: 
            
                cursor.execute(
                    """
                    DROP TABLE IF EXISTS users;
                    CREATE TABLE users (
                        user_id VARCHAR(100) PRIMARY KEY,
                        age INTEGER NOT NULL,
                        gender VARCHAR(20) NOT NULL,
                        country VARCHAR(100) NOT NULL,
                        city VARCHAR(100) NOT NULL,
                        signup_date DATE NOT NULL,
                        income_level VARCHAR(50) NOT NULL,
                        preferred_category VARCHAR(100) NOT NULL,
                        loyalty_tier VARCHAR(50) NOT NULL
                     
                    );
                    """

                )
                cursor.execute(
                    """
                    DROP TABLE IF EXISTS products;
                    CREATE TABLE IF NOT EXISTS products (
                        product_id VARCHAR PRIMARY KEY,
                        product_name VARCHAR NOT NULL,
                        product_description TEXT NOT NULL,
                        category VARCHAR NOT NULL,
                        subcategory VARCHAR NOT NULL,
                        brand VARCHAR NOT NULL,
                        price NUMERIC NOT NULL,
                        rating_avg FLOAT,           
                        review_count INTEGER NOT NULL,
                        stock_quantity INTEGER NOT NULL,
                        date_added TIMESTAMP NOT NULL

                    )
                    """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS purchases;
                    CREATE TABLE IF NOT EXISTS purchases(
                        purchase_id VARCHAR PRIMARY KEY,
                        order_id VARCHAR NOT NULL,
                        user_id VARCHAR NOT NULL,
                        product_id VARCHAR NOT NULL,
                        session_id VARCHAR,
                        interaction_id VARCHAR,
                        quantity INTEGER NOT NULL,
                        unit_price NUMERIC(10,2) NOT NULL,
                        total_amount NUMERIC(10,2) NOT NULL,
                        order_date TIMESTAMP NOT NULL
                    )
                    """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS reviews;
                    CREATE TABLE IF NOT EXISTS reviews(
                        review_id VARCHAR PRIMARY KEY,
                        user_id VARCHAR NOT NULL,
                        product_id VARCHAR NOT NULL,
                        purchase_id VARCHAR NOT NULL,
                        rating INTEGER NOT NULL,
                        title VARCHAR(255),
                        review_text TEXT,
                        review_date TIMESTAMP NOT NULL
                    )
                    """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS sessions;
                    CREATE TABLE IF NOT EXISTS sessions(
                        session_id VARCHAR PRIMARY KEY,
                        user_id VARCHAR NOT NULL,
                        start_time TIMESTAMP NOT NULL,
                        device_type VARCHAR(50),
                        referrer_source VARCHAR(100),
                        is_converted BOOLEAN
                    )
                    """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS interactions;
                    CREATE TABLE IF NOT EXISTS interactions(
                        interaction_id VARCHAR PRIMARY KEY,
                        user_id VARCHAR NOT NULL,
                        product_id VARCHAR NOT NULL,
                        session_id VARCHAR NOT NULL,
                        interaction_type VARCHAR(50) NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        dwell_time_ms INTEGER
                    )
                    """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS stg_rejects;
                    CREATE TABLE IF NOT EXISTS stg_rejects(
                        source_name TEXT NOT NULL,
                        raw_payload JSONB NOT NULL,
                        reason TEXT NOT NULL,
                        rejected_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                    """
                )

    except psycopg2.Error as e:
        # using `with conn`, any exception will cause an automatic rollback.
        # don't need to explicitly call rollback unless outside a with block.
        print(f"An error occurred: {e}")

    finally:
        #ensure the connection is always closed 
        conn.close() 

def insert_rejects(source, payload, reason):
    """Insert a rejected row into the staging rejects table.

    Parameters:
        source (str): Name of the source dataset where the rejection occurred.
        payload (tuple): The row values being rejected.
        reason (str): The reason for the rejection.
    """
    conn = connect()
    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO stg_rejects (
                        source_name,
                        raw_payload,
                        reason,
                        rejected_at
          
                    ) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """
                payload = tuple(None if pd.isna(x) else x for x in payload)
                data = (source, json.dumps(payload, default=str), reason)
                
                cursor.execute(insert_query, data) 
                #print("Rows inserted:", cursor.rowcount)
                
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
    finally:
        conn.close()

     
def insert_users_data(users_cleaned):
    """Insert cleaned user records into the users table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        users_cleaned (pandas.DataFrame): Cleaned users dataset.
    """
    #logger.info("Inserting users data into the database.")
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO users (
                        user_id,
                        age,
                        gender,
                        country,
                        city,
                        signup_date,
                        income_level,
                        preferred_category,
                        loyalty_tier
          
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(users_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except Exception as e:
                        logger.error(
                            f"Failed inserting user {value[0]}: {e}"
                        )
                        insert_rejects('users', value, str(e))
                logger.info("Finished inserting users")

                
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")

    finally:
        conn.close()

def insert_products_data(products_cleaned):
    """Insert cleaned product records into the products table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        products_cleaned (pandas.DataFrame): Cleaned products dataset.
    """
    #logger.info("Inserting products data into databadse")
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO products (
                        product_id, product_name, product_description, category, 
                        subcategory, brand, price, rating_avg, review_count, stock_quantity, 
                        date_added
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(products_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except :
                        logger.error(
                            f"Failed inserting products {value[0]}: {e}"
                        )
                        insert_rejects('products', value, str(e))
                logger.info("Finished inserting products")

    except psycopg2.Error as e:
        print(f"An error occurred while inserting products: {e}")
    finally:
        conn.close()


def insert_purchases_data(purchases_cleaned):
    """Insert cleaned purchase records into the purchases table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        purchases_cleaned (pandas.DataFrame): Cleaned purchases dataset.
    """
    #logger.info("Inserting purchases data into database")
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO purchases (
                        purchase_id, order_id, user_id, product_id, session_id, 
                        interaction_id, quantity, unit_price, total_amount, order_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(purchases_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except :
                        logger.error(
                            f"Failed inserting purchases {value[0]}: {e}"
                        )
                        insert_rejects('purchases', value, str(e))
                logger.info("Finished inserting purchases")

    except psycopg2.Error as e:
        print(f"An error occurred while inserting purchases: {e}")
    finally:
        conn.close()


def insert_reviews_data(reviews_cleaned):
    """Insert cleaned review records into the reviews table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        reviews_cleaned (pandas.DataFrame): Cleaned reviews dataset.
    """
    #logger.info("Inserting reviews data into database")
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO reviews (
                        review_id, user_id, product_id, purchase_id, rating, 
                        title, review_text, review_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(reviews_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except :
                        logger.error(
                            f"Failed inserting reviews {value[0]}: {e}"
                        )
                        insert_rejects('reviews', value, str(e))
                logger.info("Finished inserting reviews")

    except psycopg2.Error as e:
        print(f"An error occurred while inserting reviews: {e}")
    finally:
        conn.close()


def insert_sessions_data(sessions_cleaned):
    """Insert cleaned session records into the sessions table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        sessions_cleaned (pandas.DataFrame): Cleaned sessions dataset.
    """
    #logger.info('Inserting sessions into the database')
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO sessions (
                        session_id, user_id, start_time, device_type, 
                        referrer_source, is_converted
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(sessions_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except :
                        logger.error(
                            f"Failed inserting sessions {value[0]}: {e}"
                        )
                        insert_rejects('sessions', value, str(e))
                logger.info("Finished inserting sessions")
                
    except psycopg2.Error as e:
        print(f"An error occurred while inserting sessions: {e}")
    finally:
        conn.close()


def insert_interactions_data(interactions_cleaned):
    """Insert cleaned interaction records into the interactions table.

    Rows that fail insertion are logged and written to `stg_rejects`.

    Parameters:
        interactions_cleaned (pandas.DataFrame): Cleaned interactions dataset.
    """
    #logger.info('Inserting interactions data into the database')
    conn = connect()

    try: 
        with conn:
            with conn.cursor() as cursor:

                # Define the SQL INSERT statement with placeholders
                insert_query = """
                    INSERT INTO interactions (
                        interaction_id, user_id, product_id, session_id, interaction_type, 
                        timestamp, dwell_time_ms
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                data_tuples = list(interactions_cleaned.itertuples(index=False, name=None))
                for value in data_tuples:
                    try:
                        cursor.execute(insert_query, value)
                    except :
                        logger.error(
                            f"Failed inserting interactions {value[0]}: {e}"
                        )
                        insert_rejects('interactions', value, str(e))
                logger.info("Finished inserting interactions")
                
    except psycopg2.Error as e:
        print(f"An error occurred while inserting interactions: {e}")
    finally:
        conn.close()



    


    
    


    
    


    
    
    