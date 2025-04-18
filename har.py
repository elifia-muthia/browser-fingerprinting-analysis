from seleniumwire import webdriver  # Import Selenium Wire's webdriver
import time, pathlib

"""
Set up Chrome Driver
"""
# Configure Chrome options if needed (here, we keep it basic)
chrome_options = webdriver.ChromeOptions()

"""
Set Selenium Wire options
"""
seleniumwire_options = {
    "enable_har": True
}  # This enables HAR recording of all network traffic

driver = webdriver.Chrome(
    options=chrome_options, seleniumwire_options=seleniumwire_options
)

"""
Visiting YouTube
"""
# The driver waits until the page is fully loaded
url = "https://www.youtube.com"
driver.get(url)

# Wait for the driver to log more network activities after it's fully loaded
wait_time = 20
print(f"Waiting for {wait_time} on {url}")
time.sleep(wait_time)

# After browsing, retrieve the HAR data from Selenium Wire
har_data = driver.har

# Export the HAR data to a file in JSON format
timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
outfile = pathlib.Path(f"youtube_{timestamp}.har.json")
with outfile.open("w", encoding="utf-8") as har_file:
    har_file.write(har_data)
    har_file.flush()

print(f"HAR written to {outfile.resolve()}")

"""
Close Browser
"""
driver.quit()
