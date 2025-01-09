# rimmonim_translation.py:
from sefaria_translation.sefaria_api.fetch_sefaria_text import fetch_sefaria_text, clean_text
from sefaria_translation.chapter_translator import ChapterTranslator
from sefaria_translation.text_reference import TextReference, ChapterReference
from sefaria_translation.save_translation import SaveTranslation
from pathlib import Path
import json
from typing import TypeGuard

def is_list_of_str_lists(obj: object) -> TypeGuard[list[list[str]]]:
    return (isinstance(obj, list) and
            all(isinstance(x, list) and all(isinstance(s, str) for s in x) for x in obj))


def fetch_gate (gate_num: int) -> list[list[str]]:
    gate_ref = TextReference("Pardes_Rimmonim", gate_num)
    gate_ref.section_name = "Gate"
    gate_text = fetch_sefaria_text(gate_ref)
    if not is_list_of_str_lists(gate_text):
        raise TypeError("Expected list[list[str]]")
    return [clean_text(chapter) for chapter in gate_text]


def translate_chapter (chapter_text: list[str], gate_num: int, chapter_num: int ) -> list[tuple[str, str]]:

    chapt_ref = ChapterReference("Pardes_Rimmonim", gate_num, chapter_num)
    chapt_ref.section_name = "Gate"
    translator = ChapterTranslator(chapt_ref, chapter_text)
    translation:list[tuple[str, str]] = translator.translate_chapter()
    return translation

def save_chapter_translation(translation: list[tuple[str, str]], gate_num: int, chapter_num: int) -> None:
    # Create directory structure if it doesn't exist
    save_dir = Path("saved_translations_json/pardes_rimmonim")
    save_dir.mkdir(parents=True, exist_ok=True)

    # Create filename
    filename = f"pardes_rimmonim_{gate_num}_{chapter_num}.json"
    filepath = save_dir / filename

    # Convert list of tuples to list of dictionaries for better JSON formatting
    translation_dict = {
        "title": "Pardes Rimmonim",
        "gate_num": gate_num,
        "chapter_num": chapter_num,
        "translation": [{"hebrew": heb, "english": eng} for heb, eng in translation]
    }

    # Write to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(translation_dict, f, ensure_ascii=False, indent=2)

def check_translation_exists(gate_num: int, chapter_num: int) -> bool:
    save_dir = Path("saved_translations_json/pardes_rimmonim")
    filename = f"pardes_rimmonim_{gate_num}_{chapter_num}.json"
    filepath = save_dir / filename
    return filepath.exists()

def translate_gate(gate_num: int):
    gate_text = fetch_gate(gate_num)


    for i, chapter_text in enumerate(gate_text):
        chapter_num = i + 1
        if check_translation_exists(gate_num, chapter_num):
            print(f"Skipping Gate {gate_num} Chapter {chapter_num} - translation already exists")
            continue

        print(f"\nTranslating gate {gate_num}, chapter {chapter_num} / {len(gate_text)}.")
        print(f"Chapter {chapter_num} has {len(chapter_text)} passages.")

        translated_chapter: list[tuple[str, str]] = translate_chapter(chapter_text, gate_num, chapter_num)
        save_chapter_translation(translated_chapter, gate_num, chapter_num)




def main() -> None:

    # Meditation and divine names
    translate_gate(21)
    translate_gate(27)
    translate_gate(30)

    # Mystical communion
    translate_gate(32)

    # Prophecy
    translate_gate(24)
    translate_gate(31)


if __name__ == "__main__":
    main()