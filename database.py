import mysql.connector
from mysql.connector import Error

def get_missing_data_drug_codes():
    try:
        connection = mysql.connector.connect(
            host='msam.lmu.build',
            database='msamlmub_CapitolDrugs',
            user='msamlmub_cd',
            password='Capit01_D2023'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            #cursor.execute("SELECT * FROM NewMasterSheet LIMIT 0, 100;")
            cursor.execute("SELECT DISTINCT NDC FROM MasterSheet")
            fetch = cursor.fetchall()
            for row in fetch:
                # Get values in CIN columns
                print(row)
            #print(fetch)
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
get_missing_data_drug_codes()