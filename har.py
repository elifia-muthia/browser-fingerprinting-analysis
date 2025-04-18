# from selenium import webdriver
# import undetected_chromedriver as uc
from seleniumwire import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import time
import json, datetime, pathlib

"""
Set up Chrome Driver
"""

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

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
outfile   = pathlib.Path(f"youtube_{timestamp}.har.json") 
with outfile.open("w", encoding="utf-8") as f:
    json.dump(har, f, indent=2)

print(f"HAR written to {outfile.resolve()}")

"""
Close Browser
"""
driver.quit()
