# Usage in main.py:
from sefaria_api import fetch_sefaria_text
from translate import ChapterTranslator
from text_reference import TextReference


def main() -> None:
    # Fetch and prepare text
    text_ref = TextReference("Pardes_Rimmonim", 30, 1)
    text_ref.section_name = "Gate"

    chapter: list[str] = fetch_sefaria_text(text_ref)

    # Initialize translator
    translator = ChapterTranslator(text_ref, chapter)

    original = chapter[0]
    translation = translator.translate_passage()

    print(f"\nPassage {1}:")
    print(f"Original: {original}")
    print(f"Translation: {translation}")
    print("-" * 80)


if __name__ == "__main__":
    main()
