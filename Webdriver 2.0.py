from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

print(driver.title)

# Sleep for 10 seconds
time.sleep(10)

driver.quit()
