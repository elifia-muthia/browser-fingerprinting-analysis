from seleniumwire import webdriver
import time
import os
import shutil
import json


class HAR_chrome:
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    user_profile = None

    driver = None
    start_time = None

    def __init__(self, choose_profile=False):
        # list all profiles

        chrome_options = webdriver.ChromeOptions()
        selenium_options = {"enable_har": True}

        if choose_profile:
            self.select_profile()

        if self.user_profile:
            print(f"Using profile: {self.user_profile}")
            print(f"User data directory: {self.user_data_dir}")
            chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={self.user_profile}")

        self.driver = webdriver.Chrome(
            options=chrome_options, seleniumwire_options=selenium_options
        )
        self.start_time = time.localtime()

    def select_profile(self):
        # Set the path to your Chrome user data directory
        local_state_path = os.path.join(self.user_data_dir, "Local State")

        # Read Local State JSON to get profile metadata
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)

        profiles = local_state["profile"]["info_cache"]

        print("Which profile do you want to use?")
        print("Available profiles:")
        print("0: Create new profile")
        for i, (profile_dir, info) in enumerate(profiles.items(), start=1):
            print(f"{i}: {info['name']}")

        # Get the profile number from the user
        profile_number = input("Enter the profile number: ")
        if profile_number == "0":
            # Create a new profile
            profile_name = input("Enter the new profile name: ")
            created = False
            while not created:
                created = self.create_new_profile(profile_name)
        else:
            # Check if the input is valid
            if (
                not profile_number.isdigit()
                or int(profile_number) < 1
                or int(profile_number) > len(profiles)
            ):
                print("Invalid input. Please enter a valid profile number.")
                return

            # Get the selected profile directory
            selected_profile = list(profiles.keys())[int(profile_number) - 1]
            self.user_profile = selected_profile
            print(f"Selected profile: {profiles[selected_profile]['name']}")

    # check if the profile already exists or not
    # if not exists, ask the user if they want to create a new profile
    # by getting the answer from the user
    def create_new_profile(self, profile_name):
        # Create a new profile directory
        new_profile_path = os.path.join(self.user_data_dir, profile_name)
        if not os.path.exists(new_profile_path):
            os.makedirs(new_profile_path)
            print(f"New profile created at: {new_profile_path}")
            return True

        print(f"Profile {profile_name} already exists at: {new_profile_path}")
        return False

    def delete_current_profile(self):
        profile_path = os.path.join(self.user_data_dir, self.user_profile)
        print("Are you sure you want to delete profile?")
        print(f"Current profile path: {profile_path}")
        delete_input = input("Type 'yes' to confirm: ")
        if delete_input.lower() == "yes":
            shutil.rmtree(profile_path)
            print(f"Profile {self.user_profile} deleted.")
        else:
            print("Profile is not deleted.")

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
