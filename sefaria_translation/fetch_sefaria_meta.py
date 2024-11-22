# api_client.py
import requests
from sefaria_translation.schemas.whole_text_meta import WholeTextMeta
from sefaria_translation.schemas.sefaria_index import SefariaIndex


index_endpoint: str = "https://www.sefaria.org/api/v2/raw/index"


def fetch_sefaria_meta(title: str, authors_display_names: str = "") -> WholeTextMeta:
    url = f"{index_endpoint}/{title}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 400/500 status codes
        data: SefariaIndex = response.json()
        if not isinstance(data, dict):
            raise ValueError("Response is not a dictionary")
        return WholeTextMeta.from_json(data, authors_display_names, title)
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from Sefaria API: {str(e)}")


# Usage example:
# this if statement checks if the file is run directly.
if __name__ == "__main__":
    # client = SefariaClient()

    try:
        # result = fetch_sefaria_text("Pardes_Rimmonim", 30, 1)
        # text = result["text"]
        # print(result["versions"][0]["text"])
        # cleaned = clean_text( result)
        metadata = fetch_sefaria_meta("Pardes_Rimmonim", "Moses ben Jacob Cordovero")
        print(metadata)
        # chapter1 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4))
        # passage4 = fetch_sefaria_text(TextReference("Pardes_Rimmonim", 30, 1, 4), 3)
        # print(chapter1[3] == passage4)
        # print(result)
    except Exception as e:
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        print("\nError details:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
