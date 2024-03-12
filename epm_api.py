import requests
import pandas as pd
from cryptography.fernet import Fernet


def runEpmQueryApi(sql_query: str, key: str, cirrusHostname: str):
    # Initialize the Fernet cipher with the key
    cipher = Fernet(key)

    encrypted_sql = cipher.encrypt(sql_query.encode())
    encrypted_sql = encrypted_sql.decode('utf-8')
    
    url = f'https://{cirrusHostname}/spend/get_data'
    headers = {
        'Content-type': 'application/json'
    }

    data = {
        'string_value': encrypted_sql
    }

    query_data_response = requests.post(url=url, headers=headers, json=data)

    if query_data_response.status_code == 200:
        #return dataframe 
        df = pd.read_json(query_data_response.json().get('result'))
        return df
    
    return query_data_response.status_code
    