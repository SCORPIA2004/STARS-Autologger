import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup

# Set the path to the chromedriver.exe file
chromedriver_path = './chromedriver.exe'

# Set the username and password for the STARS account and the Bilkent webmail account
stars_username = '22101343'
stars_password = 'C9NAXC'
webmail_username = 'shayan.usman@ug.bilkent.edu.tr'
webmail_password = '0ZezSHZi'

# Set the URL for the STARS login page and the webmail login page
stars_url = 'https://stars.bilkent.edu.tr/srs/'
webmail_url = 'https://webmail.bilkent.edu.tr/'

# Set the browser options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Open the STARS login page
driver.get(stars_url)

# Enter the STARS username and password
username_field = driver.find_element_by_id('LoginForm_username')
username_field.send_keys(stars_username)
password_field = driver.find_element_by_id('LoginForm_password')
password_field.send_keys(stars_password)
password_field.send_keys(Keys.RETURN)

# Open a new tab and go to the webmail login page
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(webmail_url)

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

# # Fetch the verification code from the inbox
# response = requests.get(webmail_url)
# soup = BeautifulSoup(response.content, 'html.parser')
# verification_code = soup.find('span', {'class': 'verimaci_kodu'})

# Wait for the inbox to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "messagelist-header")))

# Find the most recent email with the subject "Secure Login Gateway E-Mail Verification Code"
email = driver.find_element_by_xpath('//td[contains(.//span[@class="subject"], "Secure Login Gateway E-Mail Verification Code")]')

# Click on the email to open it
email.click()

# Wait for the page to load completely
WebDriverWait(driver, 3).until(lambda d: d.execute_script('return document.readyState') == 'complete')

# Wait for the expected element to be present
try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "messagelist-header")))
except TimeoutException:
    print("Error: Timeout occurred while waiting for page to load.")

# Get the verification code from the email
# verification_code = driver.find_element_by_xpath('//div[@class=pre and contains(text(), "Verification Code:")]/text()').split()[-1]
# verification_div = driver.find_element_by_class_name('div.pre')
# verification_code = verification_div.text.split()[-2]

# switch to iframe
iframe = driver.find_element_by_id('messagecontframe')
driver.switch_to.frame(iframe)

# search for element inside iframe
# verification_code_element = driver.find_element_by_xpath('//html//body//div[@class="pre" and contains(text(), "Verification Code:")]')
try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "messagebody")))
except TimeoutException:
    print("Error: Timeout occurred while waiting for page to load.")

verification_code_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div')
verification_code = verification_code_element.text.split()[2]

# switch back to main document
driver.switch_to.default_content()


# Return to the previous tab and enter the verification code in the appropriate field
driver.switch_to.window(driver.window_handles[0])
verification_code_field = driver.find_element_by_id('EmailVerifyForm_verifyCode')
verification_code_field.send_keys(verification_code)

# Print a message confirming that the verification code has been fetched

verify_button = driver.find_element_by_class_name("btn-bilkent")
verify_button.click()


# Close the browser
# driver.quit()
