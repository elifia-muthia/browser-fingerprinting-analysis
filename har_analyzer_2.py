import requests
import json
from haralyzer import HarParser


def load_tracker_domains(tracker_list_path):
    """
    Load tracker domains from DuckDuckGo's tracker blocklist JSON file.
    Returns a set of domains.
    """
    with open(tracker_list_path, "r", encoding="utf-8") as f:
        tracker_data = json.load(f)
    # The blocklist format has a 'trackers' dict with domains as keys
    return set(tracker_data.get("trackers", {}).keys())


def domain_from_url(url):
    """
    Extract the domain from a URL.
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    return parsed.hostname


def analyze_har_with_trackers(har_file_path, tracker_domains):
    """
    Analyze the HAR file for requests to known tracker domains.
    """
    suspicious_entries = []
    with open(har_file_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)
    har_parser = HarParser(har_data)
    for page in har_parser.pages:
        for entry in page.entries:
            url = entry["request"]["url"]
            domain = domain_from_url(url)
            if domain in tracker_domains:
                suspicious_entries.append(
                    {
                        "url": url,
                        "domain": domain,
                        "status": entry["response"].get("status"),
                    }
                )
    return suspicious_entries


if __name__ == "__main__":
    har_file = "20250420-024719-20250420-024752.har"  # Path to your HAR file
    tracker_list = "extension-tds.json"  # Path to DuckDuckGo tracker blocklist
    tracker_domains = load_tracker_domains(tracker_list)
    results = analyze_har_with_trackers(har_file, tracker_domains)
    if results:
        print("Requests to known tracker domains detected:")
        for entry in results:
            print(f"URL: {entry['url']}")
            print(f"Domain: {entry['domain']}")
            print(f"Status Code: {entry['status']}")
            print("-" * 50)
    else:
        print("No requests to known tracker domains found in the HAR file.")
