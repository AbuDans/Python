from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#ENTER credentials
EMAIL = ''
PASSWORD = ''
NUMBER=''
Tweet = "https://twitter.com/Microsoft/status/1806364370173096043"


PATH = "chromedriver.exe"
service = Service(PATH)
driver = webdriver.Chrome(service=service)


driver.get("https://x.com/i/flow/login")


wait = WebDriverWait(driver, 15)  
email_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
email_field.clear()
email_field.send_keys(EMAIL)
email_field.send_keys(Keys.RETURN)


wait = WebDriverWait(driver, 15)  
password_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
password_field.clear()
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)


expected_url = "https://x.com/home"
wait2 = WebDriverWait(driver, 10)
wait2.until(EC.url_changes("https://x.com/i/flow/login"))
current_url = driver.current_url

if current_url == expected_url:
    print("Login successful!")
    driver.get(Tweet)
    target_element = wait.until(EC.visibility_of_element_located((
    By.XPATH, 
    "//div[@aria-label='Timeline: Conversation']/div[1]/div[3]/div[1]/div[1]//article[@role='article']//div//div//div[2]/div[2]/div[2]"
    )))
    span_elements = parent_div.find_elements(By.XPATH, ".//span")
    all_text = " ".join([span.text for span in span_elements])
    print(all_text)




else:
    print("Login failed. Current URL: {current_url}")
#//div[@aria-label='Timeline: Conversation']/div[1]/div[3]/div[1]/div[1]//article[@role='article']//div//div//div[2]/div[2]/div[2]
#//main[@role='main']//div[@aria-label='Home timeline']/div[1]/following-sibling::section[@aria-labelledby='accessible-list-0'][1]//div[@aria-label='Timeline: Conversation']/div[1]/div[3]/div[1]/div[1]//article[@role='article']//div//div//div[2]/div[2]/div[2]
driver.close()
