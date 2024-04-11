from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import the Keys class for keyboard interactions
import time  # Import the time module
import mysql.connector
#import Webdriver_2_0.py
from mysql.connector import Error

# Path to the chromedriver executable (you need to download this separately)
chromedriver_path = '/Users/adarshreddy/Desktop/chromedriver-mac-arm64/chromedriver'

# Set up Chrome options (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # To run Chrome in headless mode (without opening a window)

# Initialize the Chrome WebDriver with options
# driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
driver = webdriver.Chrome()

driver.get('https://pdlogin.cardinalhealth.com/signin?TYPE=33554432&REALMOID=06-000b3ff8-f6e2-1c76-a58f-24d80a310000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=mqfw03tvxPqy26CpvJlRXLvMutCBCiLDBsehyGRfHw0UTDxB7OJhfKqhTBY9nu1umX0rK79RYANFXWXZENACWPv6kX8m0p0p&TARGET=-SM-https%3a%2f%2forderexpress%2ecardinalhealth%2ecom%2feps%2fmycah')

    
# Wait for the username element to be visible
wait = WebDriverWait(driver, 30)
username_element = wait.until(EC.visibility_of_element_located((By.ID, 'okta-signin-username')))

# Input username 'Capitol_Weho'
username_element.send_keys('Capitol_Weho')

# Find and input password
password_element = driver.find_element(By.ID, 'okta-signin-password')
password_element.send_keys('Raja8578!')

# Find and click submit button
submit_button = driver.find_element(By.ID, 'okta-signin-submit')
submit_button.click()

def scrape_data(cin):
    # Wait for the search bar element to be clickable
    search_bar = wait.until(EC.element_to_be_clickable((By.ID, 'viewns_Z7_23F6KHG30GG980IKD2NS6Q00C6_:searchbarSubview:searchbarForm:endeca_search_box_input')))
    # Click on the search bar
    search_bar.click()
    search_bar.clear()

    # Type the desired text
    search_bar.send_keys(cin)

    # Press the "Enter" key
    search_bar.send_keys(Keys.ENTER)

    # Pause for 5 seconds
    time.sleep(5)

    cin_text = f"//a[@href='{cin}']"
    anchor_element = driver.find_element(By.XPATH, cin_text)
    anchor_element.click()

    time.sleep(5)

    element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pricing Information')]")))
    elements2 = driver.find_elements(By.CLASS_NAME,"invoiceCost")
    cost = 0
    for el in elements2:
        if (el.text.startswith("$")):
            cost = el.text.replace("$","")
            cost = cost.replace(",","")


    # Generic Name
    elements2 = driver.find_elements(By.CLASS_NAME,"outputText")
    gen_name = ""
    elGenName = driver.find_element(By.XPATH, "//span[contains(@id, 'txtGenName')]")
    gen_name = elGenName.text

    # Description
    elements3 = driver.find_elements(By.CLASS_NAME,"outputText")
    decsr = ""
    elDescr = driver.find_element(By.XPATH, "//span[contains(@id, 'txtDescription')]")
    decsr = elDescr.text

    # CIN
    elements4 = driver.find_elements(By.CLASS_NAME,"outputText")
    cin = ""
    elCin = driver.find_element(By.XPATH, "//span[contains(@id, 'txtCin')]")
    cin = elCin.text

    #NDC
    elements5 = driver.find_elements(By.CLASS_NAME,"outputText")
    ndc = ""
    elNdc = driver.find_element(By.XPATH, "//span[contains(@id, 'txtNdc')]")
    ndc = elNdc.text

    # for el in elements2:
    #      print ("id :" + el.id)
    #      print ("text "+el.text)

    print(cost)     
    print(el.text)
    print(gen_name)
    print(decsr)
    print(cin)
    print(ndc)
    time.sleep(3)

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
                scrape_data(row[0])
            #print(fetch)
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
get_missing_data_drug_codes()


driver.quit()








# <span id="viewns_Z7_23F6KHG30O1080IK78A2NO3004_:frmProductDetails:txtInvoiceCost" class="invoiceCost">$3,808.03</span>
