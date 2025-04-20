from seleniumwire import webdriver
import time
import os


class HAR_chrome:
    driver = None
    start_time = None
    profile_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/")

    def __init__(self, profile="Default"):
        chrome_options = webdriver.ChromeOptions()
        selenium_options = {"enable_har": True}
        self.profile_path += profile
        print(self.profile_path)
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        self.driver = webdriver.Chrome(
            options=chrome_options, seleniumwire_options=selenium_options
        )

        self.start_time = time.localtime()

    def export_har(self, path=None):
        har_data = self.driver.har
        end_time = time.localtime()
        file_path = path if path else os.getcwd()
        start_time_str = time.strftime("%Y%m%d-%H%M%S", self.start_time)
        end_time_str = time.strftime("%Y%m%d-%H%M%S", end_time)
        file_path += f"/{start_time_str}-{end_time_str}.har"

        with open(file_path, encoding="utf-8", mode="w") as f:
            f.write(har_data)
            f.flush()
        return file_path

    def get(self, url, wait_time=0):
        self.driver.get(url)
        print(f"Waiting for {wait_time} seconds on {url}")
        time.sleep(wait_time)

    def quit(self):
        self.driver.quit()
