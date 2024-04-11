import mysql.connector
#import Webdriver_2_0.py
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
            cursor.execute("SELECT DISTINCT CIN FROM MasterSheet LIMIT 1,5")
            fetch = cursor.fetchall()
            for row in fetch:
                # Get values in CIN columns
                print(row[0])
            #print(fetch)
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
get_missing_data_drug_codes()