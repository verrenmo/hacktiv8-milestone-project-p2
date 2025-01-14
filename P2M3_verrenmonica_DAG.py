'''
===========================================================================================================================================
Phase 2 - Milestone 3

Name    : Verren Monica
Batch   : RMT - 038

This program is designed to automate the Extract, Transform, and Load (ETL) process of transferring data from PostgreSQL to Elasticsearch.
The dataset used is sales data from Supermarket ABC for a 3-month period.
The program consists of three main processes:

1. Fetch from PostgreSQL: The first process extracts data from PostgreSQL. The extracted data is then saved in a .csv file format.
2. Data Cleaning: The second process cleans the data, which includes removing duplicate entries, normalizing column names, 
   missing values, and changing the data type of the date column.
3. Post to Elasticsearch: The third process involves uploading the cleaned data to Elasticsearch.
============================================================================================================================================
'''

# Import Libraries
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from elasticsearch import Elasticsearch


# Basic configuration DAG owner and execution start date (November 1st, 24 )
default_args= {
    'owner': 'Verren Monica',
    'start_date': datetime(2024, 11, 1) - timedelta(hours=7)
    }

# Define the DAG object with its properties
with DAG(
    'h8-milestone3',
    description='Automatic Pipeline from PostgreSQL to Elastic Search',
    schedule_interval='10,20,30 9 * * 6', # Schedule for the DAG (every Saturday at 9.10, 9.20 and 9.30)
    default_args=default_args) as dag:

    # Marks the beginning and the end of the DAG
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    # First task: fetch data from PostgreSQL
    @task()
    def fetchFromPostgres():
        '''
        Fetch data from a PostgreSQL database and save it as a CSV file.
        - Defines the connection parameters (database name, username, password, and host).
        - Constructs the PostgreSQL connection URL using SQLAlchemy.
        - Establishes a connection to the database.
        - Executes an SQL query to fetch all rows from the table `table_m3`.
        - Converts the fetched data into a Pandas dataframe.
        - Saves the dataframe as a CSV file named 'P2M3_verrenmonica_data_raw.csv' without including the index.        
        '''
        # Create PostgreSQL connection URL
        database = "airflow"
        username = "airflow"
        password = "airflow"
        host = "postgres"
        postgresUrl = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

        # Create SQLAlchemy engine and establish connection to the database
        engine = create_engine(postgresUrl)
        conn = engine.connect()

        # Fetch data into pandas dataframe
        df = pd.read_sql('SELECT * FROM table_m3', conn)
        
        # Save the dataframe to csv file
        return df.to_csv("/opt/airflow/dags/P2M3_verrenmonica_data_raw.csv", index=False)
    
    # Second task: data cleaning
    @task()
    def dataCleaning():
        '''
        Perform data cleaning on the input CSV file and save the cleaned data.

        Steps:
        1. Read the input CSV file into a pandas dataframe.
        2. Remove duplicate rows to ensure data uniqueness.
        3. Standardize column names by converting them to lowercase and replacing spaces with underscores.
        4. Convert the 'date' column to a datetime format.
        5. Handle missing values in the dataframe:
            - For numerical columns (int64 and float64), replace missing values with the median.
            - For categorical columns (object), replace missing values with the mode.
            - For other data types, drop rows with missing values in those columns.
        6. Save the cleaned dataframe to a new CSV file named 'P2M3_verrenmonica_data_clean.csv' without including the index.
        '''
        # Data loading
        df = pd.read_csv("/opt/airflow/dags/P2M3_verrenmonica_data_raw.csv")
        
        # Remove duplicate rows
        df = df.drop_duplicates()

        # Standarize column names
        df.columns = df.columns.str.lower().str.replace(" ","_")

        # Convert date column to datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Function to handle missing value
        def missingValueHandling(df):
            '''
            This function is to handle missing values in a pandas dataframe based on column data types.

            Parameters:
            df (pd.DataFrame): The input dataframe with potential missing values.

            Returns:
            pd.DataFrame: The dataframe with missing values handled.
            
            Logic:
            - For numerical columns (int64, float64): Fill missing values with the column's median.
            - For categorical columns (object): Fill missing values with the column's mode.
            - For other data types: Drop rows with missing values in those columns.
            '''
            for col in df.columns:
                if df[col].dtypes in ['int64', 'float64']:
                    # Fill missing numerical values with the median
                    df[col].fillna(df[col].median(), inplace=True)
                elif df[col].dtypes == object:
                    # Fill missing categorical values with the mode
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    # Drop rows with missing values for other data types
                    df.dropna(subset=[col], inplace=True)
            return df
        
        # Apply the missing value handling function
        df = missingValueHandling(df)

        # Save the cleaned DataFrame to a new CSV file
        return df.to_csv("/opt/airflow/dags/P2M3_verrenmonica_data_clean.csv", index=False)

    # 3rd task: post data to Elasticsearch
    @task()
    def toElasticSearch():
        '''
        This function connects to an Elasticsearch server, reads a CSV file containing cleaned data,
        and uploads each row as a JSON document to the specified index. It verifies the connection
        to Elasticsearch, converts each row to JSON format, and inserts it into the "transaction" index.
        '''
        # Initialize connection
        es = Elasticsearch("http://elasticsearch:9200")
        print("Connected to Elasticsearch:", es.info())

        # Read cleaned data
        df = pd.read_csv("/opt/airflow/dags/P2M3_verrenmonica_data_clean.csv")
        
        # Convert to json and post
        for i, r in df.iterrows():
            doc=r.to_json()
            res=es.index(index="transaction", doc_type="doc", body=doc)
            print(res)
        
        # Indicate that all records have been posted
        print(">>Posted to Elastic Search<<")

    # Define the task dependencies for the DAG execution flow:
    start >> fetchFromPostgres() >> dataCleaning() >> toElasticSearch() >> end