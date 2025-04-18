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

options = {"enable_har": True}

driver = webdriver.Chrome(seleniumwire_options=options)

"""
Youtube
"""
# The driver waits until the page is fully loaded
driver.get("https://www.youtube.com")

# Wait for the driver to log more network activities after it's fully loaded
time.sleep(20)

har = driver.har

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
outfile = pathlib.Path(f"youtube_{timestamp}.har.json")
with outfile.open("w", encoding="utf-8") as f:
    f.write(har)
    f.flush()

print(f"HAR written to {outfile.resolve()}")

"""
Close Browser
"""
driver.quit()
