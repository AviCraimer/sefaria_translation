# api_client.py
import requests
import re
from typing import TypedDict, Union
from sefaria_translation.text_reference import TextReference, ReferenceLevel
from pathlib import Path


class SefariaTextVersion(TypedDict):
    text: list[str]
    # ... other fields if needed


class SefariaTextResponse(TypedDict):
    versions: list[SefariaTextVersion]


class SefariaIndex(TypedDict):
    # Add fields from response here as needed
    pass


index_endpoint: str = "https://www.sefaria.org/api/v2/raw/index"
texts_endpoint: str = "https://www.sefaria.org/api/v3/texts"


def fetch_sefaria_index(title: str) -> SefariaIndex:
    url = f"{index_endpoint}/{title}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 400/500 status codes
        data: SefariaIndex = response.json()
        if not isinstance(data, dict):
            raise ValueError("Response is not a dictionary")
        return data
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from Sefaria API: {str(e)}")


def fetch_sefaria_text(text_ref: TextReference) -> Union[list[str], list[list[str]]]:
    """
    Fetches text from Sefaria API

    Returns:
        dict: API response data
    """
    level = text_ref.ref_level
    url = f"{texts_endpoint}/{text_ref.to_url_path(level)}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 400/500 status codes
        data: SefariaTextResponse = response.json()

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
        index_data = fetch_sefaria_index("Pardes_Rimmonim")
        print(index_data)
        # chapter1 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4))
        # passage4 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4), 3)
        # print(chapter1[3] == passage4)
        # print(result)
    except Exception as e:
        print(f"Error: {e}")


sdfsd = [
    {
        "section": "Ramak",
        "heTitle": "פרדס רמונים",
        "title": "Pardes Rimmonim",
        "length": 32,
        "chapters": [
            [11, 11, 6, 6, 6, 12, 6, 4, 3, 5],
            [14, 8, 15, 3, 7, 1, 16],
            [8, 9, 11, 10, 7, 5, 10, 10],
            [8, 11, 8, 11, 10, 4, 11, 3, 10, 7],
            [6, 9, 3, 13, 16, 8],
            [17, 13, 7, 1, 4, 9, 8, 7],
            [8, 25, 5, 7, 7],
            [
                10,
                9,
                6,
                9,
                13,
                9,
                3,
                4,
                9,
                4,
                11,
                14,
                12,
                8,
                4,
                10,
                10,
                4,
                11,
                8,
                14,
                15,
                6,
                9,
                8,
                10,
            ],
            [5, 1, 6, 5, 7, 9],
            [6, 6, 10, 3, 6],
            [6, 8, 5, 7, 6, 8, 7],
            [10, 67, 19, 9, 15, 12],
            [66, 2, 15, 2, 3, 5, 8],
            [8, 7, 7, 11],
            [7, 5, 5, 7, 6],
            [11, 4, 10, 10, 6, 8, 4, 9, 4],
            [16, 4, 4, 5],
            [9, 4, 3, 12, 8, 7],
            [5, 4, 2, 8],
            [19, 7, 5, 1, 5, 6, 5, 4, 7, 5, 2, 6, 12],
            [5, 10, 10, 5, 9, 6, 4, 17, 6, 2, 9, 8, 12, 10, 16, 11],
            [8, 6, 7, 13],
            [
                244,
                43,
                31,
                25,
                27,
                11,
                18,
                107,
                20,
                49,
                39,
                28,
                116,
                42,
                26,
                69,
                25,
                31,
                33,
                43,
                88,
                46,
            ],
            [6, 6, 1, 3, 1, 5, 4, 10, 3, 12, 8, 6, 6, 5, 6],
            [7, 5, 5, 11, 3, 7, 6],
            [4, 2, 1, 1, 1, 1, 1, 7],
            [
                6,
                10,
                4,
                6,
                5,
                1,
                2,
                2,
                2,
                4,
                4,
                3,
                5,
                4,
                3,
                4,
                1,
                1,
                1,
                3,
                3,
                1,
                2,
                1,
                1,
                4,
                9,
            ],
            [6, 3, 8, 2, 3, 10],
            [9, 6, 7, 13, 5],
            [4, 1, 2, 4, 35, 7, 4, 12],
            [10, 6, 8, 8, 10, 6, 7, 12, 9, 10, 5],
            [9, 5, 4],
        ],
        "book": "Pardes Rimmonim",
        "heBook": "פרדס רמונים",
    }
]
