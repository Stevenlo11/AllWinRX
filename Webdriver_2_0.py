from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Define df in the global scope
df = pd.DataFrame(columns=['TradeName', 'GenericName', 'Strength', 'Size', 'Form', 'Price', 'ERC'])
not_found_count = 0  # Initialize counter for not found values outside the loop

chromedriver_path = '/Users/adarshreddy/Desktop/chromedriver-mac-arm64/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome()

driver.get('https://pdlogin.cardinalhealth.com/signin?TYPE=33554432&REALMOID=06-000b3ff8-f6e2-1c76-a58f-24d80a310000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=mqfw03tvxPqy26CpvJlRXLvMutCBCiLDBsehyGRfHw0UTDxB7OJhfKqhTBY9nu1umX0rK79RYANFXWXZENACWPv6kX8m0p0p&TARGET=-SM-https%3a%2f%2forderexpress%2ecardinalhealth%2ecom%2feps%2fmycah')

wait = WebDriverWait(driver, 30)
username_element = wait.until(EC.visibility_of_element_located((By.ID, 'okta-signin-username')))
username_element.send_keys('Capitol_Weho')

password_element = driver.find_element(By.ID, 'okta-signin-password')
password_element.send_keys('Raja8578!')

submit_button = driver.find_element(By.ID, 'okta-signin-submit')
submit_button.click()

def scrape_data(cin):
    global not_found_count
    wait = WebDriverWait(driver, 30)
    search_bar = wait.until(EC.element_to_be_clickable((By.ID, 'viewns_Z7_23F6KHG30GG980IKD2NS6Q00C6_:searchbarSubview:searchbarForm:endeca_search_box_input')))
    search_bar.click()
    search_bar.clear()
    search_bar.send_keys(cin)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        cin_text = f"//a[@href='{cin}']"
        anchor_element = driver.find_element(By.XPATH, cin_text)
        anchor_element.click()
        time.sleep(3)

        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pricing Information')]")))
        elements2 = driver.find_elements(By.CLASS_NAME, "invoiceCost")
        cost = 0
        for el in elements2:
            if el.text.startswith("$"):
                cost = el.text.replace("$", "")
                cost = cost.replace(",", "")

        elements2 = driver.find_elements(By.CLASS_NAME, "outputText")
        gen_name = ""
        elGenName = driver.find_element(By.XPATH, "//span[contains(@id, 'txtGenName')]")
        gen_name = elGenName.text

        elements6 = driver.find_elements(By.CLASS_NAME, "outputText")
        strength = ""
        elStrength = driver.find_element(By.XPATH, "//span[contains(@id, 'txtStrength')]")
        strength = elStrength.text

        elements7 = driver.find_elements(By.CLASS_NAME, "outputText")
        size = ""
        elSize = driver.find_element(By.XPATH, "//span[contains(@id, 'txtpackageQuantity1234')]")
        size = elSize.text

        elements8 = driver.find_elements(By.CLASS_NAME, "outputText")
        form = ""
        elForm = driver.find_element(By.XPATH, "//span[contains(@id, 'txtForm')]")
        form = elForm.text

        elements9 = driver.find_elements(By.CLASS_NAME, "outputText")
        erc = ""
        try:
            elERC = driver.find_element(By.XPATH, "//span[contains(@id, 'txtEstRebate')]")
        except NoSuchElementException:
            elERC = driver.find_element(By.XPATH, "//span[contains(@id, 'txtEstRebateZero')]")
        erc = elERC.text

        elements10 = driver.find_elements(By.CLASS_NAME, "outputText")
        trade_name = ""
        elTradeName = driver.find_element(By.XPATH, "//span[contains(@id, 'txtTradeName')]")
        trade_name = elTradeName.text

        # Return all scraped data including ERC
        return trade_name, gen_name, strength, size, form, cost, erc

    except NoSuchElementException:
        not_found_count += 1
        print(f"No value found for CIN: {cin}. Total not found count: {not_found_count}")
        return None

    except Error as e:
        print(e)
    time.sleep(1)

def update_data_in_database(cin, trade_name, gen_name, strength, size, form, cost, erc):
    try:
        connection = mysql.connector.connect(
            host='msam.lmu.build',
            database='msamlmub_CapitolDrugs',
            user='msamlmub_cd',
            password='Capit01_D2023'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Update the data in the database table including ERC
            query = "UPDATE MasterSheet SET TradeName = %s, GenericName = %s, Strength = %s, Size = %s, Form = %s, Price = %s, Est_Rebate = %s WHERE CIN = %s"
            values = (trade_name, gen_name, strength, size, form, cost, erc, cin)
            cursor.execute(query, values)

            # Commit the transaction
            connection.commit()
            print("Data updated successfully.")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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
            cursor.execute(
                """
                SELECT DISTINCT CIN 
                FROM MasterSheet 
                WHERE 
                    Price IS NULL OR
                    Est_Rebate IS NULL 
                LIMIT 595,1000
                """
            )
            fetch = cursor.fetchall()

            for row in fetch:
                print(row[0])
                data = scrape_data(row[0])

                # Check if data is None before unpacking
                if data is not None:
                    # Call function to update data in the database
                    update_data_in_database(row[0], *data)

    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

get_missing_data_drug_codes()
driver.quit()
