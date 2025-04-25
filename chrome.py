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

# =======================
# CNN Interaction Session (New separate session)
# =======================

print("Starting CNN session...")


# Set up and start a new session for CNN
# cnn_service = Service(ChromeDriverManager().install())
# cnn_driver = webdriver.Chrome(service=cnn_service)

# Open CNN's homepage
driver.get("https://www.cnn.com")
time.sleep(5)  # Wait for the page to load
print("CNN homepage loaded.")


# Extract URLs for three headline articles
headlines = driver.find_elements(By.CSS_SELECTOR, "a.container__title-url")
article_urls = []
for headline in headlines:
    href = headline.get_attribute("href")
    if href:
        article_urls.append(href)
    if len(article_urls) >= 3:
        break

if not article_urls:
    print("No headlines found. The CSS selector may need to be updated.")
else:
    print("Found article URLs:")
    for url in article_urls:
        print(url)

# Open each article URL in a new browser tab
for url in article_urls:
    driver.execute_script("window.open('{}','_blank');".format(url))
    time.sleep(5)  # Brief pause between opening tabs


"""
Close Browser
"""
driver.quit()