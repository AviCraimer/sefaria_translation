# api_client.py
import requests
import re
from typing import TypedDict
from text_reference import TextReference, ReferenceLevel


class Version(TypedDict):
    text: list[str]
    # ... other fields if needed


class SefariaResponse(TypedDict):
    versions: list[Version]


texts_endpoint = "https://www.sefaria.org/api/v3/texts"


# level defaults to chapter
def fetch_sefaria_text(text_ref: TextReference, level: ReferenceLevel = 2) -> list[str]:
    """
    Fetches text from Sefaria API

    Returns:
        dict: API response data
    """
    url = f"{texts_endpoint}/{text_ref.to_url_path(level)}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 400/500 status codes
        data: SefariaResponse = response.json()

        if not isinstance(data, dict):
            raise ValueError("Response is not a dictionary")
        if "versions" not in data or not data["versions"]:
            raise ValueError("No versions in response")
        if "text" not in data["versions"][0]:
            raise ValueError("No text in version")

        return data["versions"][0]["text"]

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from Sefaria API: {str(e)}")


def clean_text(text_array: list[str]) -> list[str]:
    """
    Cleans text by removing img tags and any resulting empty strings

    Args:
        text_array: List of lists containing strings

    Returns:
        List of lists with cleaned strings, empty entries removed
    """
    img_pattern = r"<img[^>]+>"

    def clean_string(s: str) -> str:
        return re.sub(img_pattern, "", s)

    # Process each nested array and filter out empty strings
    return [clean_string(s) for s in text_array]


def join_text(text_array: list[str]) -> str:
    return "\n\n".join(text_array)


def format_text(text_array: list[str]) -> str:
    cleaned_text = clean_text(text_array)
    return join_text(cleaned_text)


# Usage example:
# this if statement checks if the file is run directly.
if __name__ == "__main__":
    # client = SefariaClient()

    try:
        # result = fetch_sefaria_text("Pardes_Rimmonim", 30, 1)
        # text = result["text"]
        # print(result["versions"][0]["text"])
        # cleaned = clean_text( result)

        chapter1 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4))
        passage4 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4), 3)
        print(chapter1[3] == passage4)
        # print(result)
    except Exception as e:
        print(f"Error: {e}")
