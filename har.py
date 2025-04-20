import time, pathlib
from har_chrome import HAR_chrome

chrome = HAR_chrome(
    "Default"
)  # Put "Profile {num}" if you want to use another profile e.g. Profile 2

"""
Visiting YouTube
"""
# The driver waits until the page is fully loaded
url = "https://www.youtube.com"
chrome.get(url, 5)

# After browsing, retrieve the HAR data from Selenium Wire
har_path = chrome.export_har()

# Export the HAR data to a file in JSON format
print(f"HAR written to {har_path}")

"""
Close Browser
"""
chrome.quit()
