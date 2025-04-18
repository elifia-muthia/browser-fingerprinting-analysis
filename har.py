# from selenium import webdriver
# import undetected_chromedriver as uc
from seleniumwire import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import time

"""
Set up Chrome Driver
"""
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

options = {
    'enable_har': True
}

driver = webdriver.Chrome(seleniumwire_options=options)

"""
Youtube
"""
driver.get("https://www.youtube.com")

time.sleep(20) # wait for page to load

har = driver.har

print(har)

"""
Close Browser
"""
driver.quit()
