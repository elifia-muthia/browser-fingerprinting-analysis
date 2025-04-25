import time, pathlib
from har_exporter import HAR_Exporter

chrome = HAR_Exporter(browser="Chrome",
    choose_profile=False
)  # Change it to True to select an existing profile

"""
Visiting YouTube
"""
# The driver waits until the page is fully loaded
url = "https://www.youtube.com"
chrome.get(url, 5)

# Visit Wall Street Journal
url = "https://www.wsj.com"
chrome.get(url, 5)

# After browsing, retrieve the HAR data from Selenium Wire
har_path = chrome.export_har()

# Export the HAR data to a file in JSON format
print(f"HAR written to {har_path}")

"""
Close Browser
"""
chrome.quit()
