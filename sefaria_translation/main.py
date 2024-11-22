# main.py:
from sefaria_translation.sefaria_api.fetch_sefaria_text import fetch_sefaria_text
from sefaria_translation.chapter_translator import ChapterTranslator
from sefaria_translation.text_reference import ChapterReference
from sefaria_translation.save_translation import SaveTranslation


def main() -> None:
    # Fetch and prepare text
    text_ref = ChapterReference("Pardes_Rimmonim", 30, 1)
    text_ref.section_name = "Gate"

    chapter: list[str] = fetch_sefaria_text(text_ref)

    # Initialize translator
    # translator = ChapterTranslator(text_ref, chapter)

    # translator.translate_chapter()
    # save = SaveTranslation(translator)
    # save.save_to_html()
    # for translatedPassage in translator.translations:
    #     print(translatedPassage + "\n" + ("-" * 80) + "\n")


if __name__ == "__main__":
    main()
