from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    # Use SQLAlchemy's create_engine to establish the connection
    return create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

def load_table(table_name):
    engine = get_connection()  # Use the SQLAlchemy engine
    df = pd.read_sql(f"SELECT * FROM {table_name} ORDER BY timestamp DESC", engine)
    return df

# Use this as get_conn() if you prefer
get_conn = get_connection

# Define the query function to fetch data from the database
def query(sql_query):
    engine = get_connection()
    df = pd.read_sql(sql_query, engine)
    return df

