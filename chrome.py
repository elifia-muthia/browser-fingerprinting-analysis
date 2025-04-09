from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

"""
Set up Chrome Driver
"""
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

"""
Youtube
"""
driver.get("https://www.youtube.com")

time.sleep(3) # wait for page to load

# search for videos on cats
search_box = driver.find_element(By.NAME, 'search_query')
search_box.send_keys("cats")
search_box.send_keys(Keys.RETURN)

time.sleep(3) # wait for page to load

# watch the first video that is not an ad
videos = driver.find_elements(By.XPATH, '//a[@id="video-title"]') # find all video links

actual_video = None
for video in videos:
    if video.get_attribute('href') and '/watch?v=' in video.get_attribute('href'): # look for actual videos
        actual_video = video
        break
actual_video.click()

time.sleep(20) # wait for video to load and play

"""
Close Browser
"""
driver.quit()
