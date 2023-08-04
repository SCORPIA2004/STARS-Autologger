import csv
import os
import time
from sys import exit
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def logMessage(em, type):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        row = [current_time, type, em]
        writer.writerow(row)

with open("log.csv", "a", newline="") as f:
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    writer = csv.writer(f)
    row = ["Time", "Type", "Message", current_time]
    writer.writerow(row)


# Set the path to the chromedriver.exe file
chromedriver_path = './chromedriver.exe'

# Set the username and password for the STARS account and the Bilkent webmail account
file_name = 'loginDetails.txt'
# check if file exists
if not os.path.isfile(file_name):
    logMessage("loginDetails.txt is missing", "Fail")
    exit(1)

login_details = {}

with open(file_name, 'r') as file:
    for line in file:
        if line.startswith("stars_username"):
            stars_username = line.split("'")[1].strip("'")
            if stars_username == "":
                logMessage("STARS username is empty", "Fail")
                exit(1)
        elif line.startswith("stars_password"):
            stars_password = line.split("'")[1].strip("'")
            if stars_password == "":
                logMessage("STARS password is empty", "Fail")
                exit(1)
        elif line.startswith("webmail_username"):
            webmail_username = line.split("'")[1].strip("'")
            if webmail_username == "":
                logMessage("Webmail username is empty", "Fail")
                exit(1)
        elif line.startswith("webmail_password"):
            webmail_password = line.split("'")[1].strip("'")
            if webmail_password == "":
                logMessage("Webmail password is empty", "Fail")
                exit(1)


logMessage("Got login details from file.", "Success")


# Set the URL for the STARS login page and the webmail login page
stars_url = 'https://stars.bilkent.edu.tr/srs/'
webmail_url = 'https://webmail.bilkent.edu.tr/'

# Set the browser options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Open the STARS login page
driver.get(stars_url)
logMessage("Opened STARS login page.", "Success")

# Enter the STARS username and password
username_field = driver.find_element_by_id('LoginForm_username')
username_field.send_keys(stars_username)
password_field = driver.find_element_by_id('LoginForm_password')
password_field.send_keys(stars_password)
password_field.send_keys(Keys.RETURN)
logMessage("Entered STARS username and password.", "Success")

# Open a new tab and go to the webmail login page
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(webmail_url)
logMessage("Opened webmail login page.", "Success")

# Wait for the webmail inbox to recieve email code
time.sleep(1)

# Enter the webmail username and password
username_field = driver.find_element_by_id('rcmloginuser')
username_field.send_keys(webmail_username)
# password_field = driver.find_element_by_id('LoginForm-')
password_field = driver.find_element_by_css_selector('[id^="LoginForm-"]')
password_field.send_keys(webmail_password)
password_field.send_keys(Keys.RETURN)

# Wait for the webmail inbox to load
time.sleep(1)

# Wait for the inbox to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "messagelist-header")))
except TimeoutException:
    # write error to a log.txt file
    logMessage("Webmail login failed. Check you username and password", "Fail")
    exit(1)
# Find the most recent email with the subject "Secure Login Gateway E-Mail Verification Code"
email = driver.find_element_by_xpath(
    '//td[contains(.//span[@class="subject"], "Secure Login Gateway E-Mail Verification Code")]')

# Click on the email to open it
email.click()

# Wait for the page to load completely
try:
    WebDriverWait(driver, 3).until(lambda d: d.execute_script('return document.readyState') == 'complete')
except TimeoutException:
    # write error to a log.txt file
    logMessage("STARS login failed. Check you verification code", "Fail")
    exit(1)

# Wait for the expected element to be present
try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "messagelist-header")))
    logMessage("Found email with verification code", "Success")
except TimeoutException:
    # write error to a log.txt file
    logMessage("Timeout occurred while waiting for page to load.", "Fail")

# switch to iframe
iframe = driver.find_element_by_id('messagecontframe')
driver.switch_to.frame(iframe)

# search for element inside iframe
try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "messagebody")))
    logMessage("Found verification code", "Success")

except TimeoutException:
    logMessage("Timeout occurred while waiting for page to load.", "Fail")

verification_code_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div')
verification_code = verification_code_element.text.split()[2]

# switch back to main document
driver.switch_to.default_content()

# Return to the previous tab and enter the verification code in the appropriate field

driver.switch_to.window(driver.window_handles[0])
verification_code_field = driver.find_element_by_id('EmailVerifyForm_verifyCode')
verification_code_field.send_keys(verification_code)

verify_button = driver.find_element_by_class_name("btn-bilkent")
verify_button.click()

# Wait for the page to load completely
WebDriverWait(driver, 3).until(lambda d: d.execute_script('return document.readyState') == 'complete')
logMessage("Successfully logged in to STARS.", "Success")