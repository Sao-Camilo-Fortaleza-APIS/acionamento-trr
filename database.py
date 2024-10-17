import pandas as pd
import oracledb
import os
from sql_p import sql
from dotenv import load_dotenv


def clear_terminal():
    # Clear the terminal based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')

def get_data():
    load_dotenv()
    IP_ADDRESS = os.environ.get("IP_ADDRESS")
    PORT = os.environ.get("PORT")
    SERVICE_NAME = os.environ.get("SERVICE_NAME")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    dsn = oracledb.makedsn(IP_ADDRESS, PORT, service_name=SERVICE_NAME)
    connection = None
    try:
        connection = oracledb.connect(user=USER, password=PASSWORD, dsn=dsn)
        df = pd.read_sql(sql, con=connection)
        print('get_data')
        return df
    except oracledb.Error as e:
        print(f'Error: {e}')
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()
