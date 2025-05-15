import pandas as pd
import oracledb
import os
from dotenv import load_dotenv


def clear_terminal():
    # Limpa o terminal
    if os.name == 'nt':  #Windows
        os.system('cls')

def get_data():
    """Função original para compatibilidade com código existente"""
    from sql_p import sql_p as sql  # Mantém comportamento original usando sql_p
    return execute_query(sql)

def execute_query(sql_query):
    """Função para executar qualquer consulta SQL passada como parâmetro"""
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
        df = pd.read_sql(sql_query, con=connection)
        print(f'Query executed successfully')
        return df
    except oracledb.Error as e:
        print(f'Error: {e}')
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()