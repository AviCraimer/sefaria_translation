# main.py:
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

    translator.translate_chapter()

    for translatedPassage in translator.translations:
        print(translatedPassage + "\n" + ("-" * 80) + "\n")


if __name__ == "__main__":
    main()
