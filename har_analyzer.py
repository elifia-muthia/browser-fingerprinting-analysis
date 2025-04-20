import json
from haralyzer import HarParser
import re

# List of keywords that may indicate fingerprinting scripts
fingerprint_keywords = [
    "canvas",
    "getimagedata",
    "todataurl",
    "webgl",
    "audiocontext",
    "fingerprint",
    "navigator.plugins",
]


def analyze_fingerprint_in_text(text):
    """
    Check if any fingerprinting keywords appear in the text.
    Returns a list of matched keywords.
    """
    text_lower = text.lower()
    return [kw for kw in fingerprint_keywords if kw in text_lower]


def analyze_har_file(har_file_path):
    """
    Load the HAR file, parse each page and its entries,
    and analyze HTTP responses for fingerprinting indicators.
    """
    suspicious_entries = []
    with open(har_file_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)

    # Create a HarParser instance from the parsed JSON data
    har_parser = HarParser(har_data)

    # Iterate over each page in the HAR file
    for page in har_parser.pages:
        for entry in page.entries:
            # Attempt to get the response content text and MIME type
            content = entry["response"].get("content", {})
            response_text = content.get("text", "")
            mime_type = content.get("mimeType", "")

            # Check if the entry is likely a script (or contains text) to analyze further
            if "javascript" in mime_type.lower() or response_text:
                matches = analyze_fingerprint_in_text(response_text)
                if matches:
                    suspicious_entries.append(
                        {
                            "url": entry["request"]["url"],
                            "status": entry["response"].get("status"),
                            "mime_type": mime_type,
                            "keywords_found": matches,
                        }
                    )

    return suspicious_entries


if __name__ == "__main__":
    har_file = (
        "20250420-024719-20250420-024752.har"  # Replace with the path to your HAR file
    )
    results = analyze_har_file(har_file)

    if results:
        print("Potential fingerprinting scripts detected:")
        for entry in results:
            print(f"URL: {entry['url']}")
            print(f"Status Code: {entry['status']}")
            print(f"MIME Type: {entry['mime_type']}")
            print(f"Keywords found: {', '.join(entry['keywords_found'])}")
            print("-" * 50)
    else:
        print("No potential fingerprinting scripts detected in the HAR file.")
