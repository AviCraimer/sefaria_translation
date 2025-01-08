# save_translation.py
import json
from pathlib import Path
from sefaria_translation.schemas.base_schema import (
    TranslatedChapter,
    TranslatedPassage,
)
from sefaria_translation.schemas.whole_text_meta import WholeTextMeta
from datetime import datetime
from sefaria_translation.text_reference import TextReference
from sefaria_translation.chapter_translator import ChapterTranslator
from typing import Literal, Optional, Tuple

OverwriteChoice = Literal["y", "n", "Y", "N"]


class SaveTranslation:
    BASE_DIR: Path = Path("saved_translations")
    _global_overwrite: Optional[Literal["Y", "N"]] = None

    def __init__(self, meta: WholeTextMeta):
        self.meta = meta

        # Create directory structure for the whole work on initialization
        self.get_whole_text_path.mkdir(parents=True, exist_ok=True)
        meta.to_file(self.get_meta_file_path)
        for section in meta.sections_meta:
            section_path: Path = self.get_section_path(section.section_num)
            section_path.mkdir(parents=True, exist_ok=True)

    @property
    def get_whole_text_path(self) -> Path:
        title: Path = self.meta.sefaria_title.lower()
        return self.BASE_DIR / title

    @property
    def get_meta_file_path(self) -> Path:
        file_name: Path = Path(f"metadata_{self.meta.sefaria_title.lower()}.json")
        return self.get_whole_text_path / file_name

    def get_section_path(self, section_num: int) -> Path:
        section_path: Path = (
            self.get_whole_text_path / f"section_{str(section_num).zfill(3)}"
        )
        return section_path

    def get_chapter_file_path(self, text_ref: TextReference) -> Path:
        """
        Gets the full path for a chapter file.

        Example:
        "saved_translations/pardes_rimmonim/section_006/pardes_rimmonim_006_003.html"
        """
        if text_ref.chapter_num is None:
            raise ValueError("Chapter Number is undefiend.")

        section_path: Path = self.get_section_path(text_ref.section_num)
        file_name = text_ref.get_file_name() + ".json"
        return section_path / file_name

    def saved_exists(self, text_ref: TextReference) -> bool:
        file_path = self.get_chapter_file_path(text_ref)
        return file_path.exists()

    def prompt_overwrite(self, file_path: Path) -> OverwriteChoice:
        """
        Prompts user whether to overwrite existing file

        Returns:
            bool: True if file should be overwritten, False otherwise
        """
        # Check if we have a global choice
        if self.__class__._global_overwrite is not None:
            return self.__class__._global_overwrite

        while True:
            choice = input(
                f"\nFile already exists: {file_path}\n"
                "Overwrite? [y/n/Y/N] "
                "(y=yes, n=no, Y=yes to all, N=no to all): "
            )

            if choice not in ["y", "n", "Y", "N"]:
                print("Invalid choice. Please enter y, n, Y, or N")
                continue

            # Handle global choices
            if choice in ["Y", "N"]:
                self.__class__._global_overwrite = choice
            return choice

    def save_chapter(self, translator: ChapterTranslator) -> Tuple[int, bool]:
        """Saves a single chapter to json"""
        text_ref = translator.text_ref
        if not translator.is_complete:
            return (text_ref.chapter_num, False)

        file_path: Path = self.get_chapter_file_path(text_ref)
        if file_path.exists() and self.prompt_overwrite(file_path).lower() == "n":
            print(f"Skipping existing: {file_path}")
            return (translator.chapter_num, True)

        translation_tuples = enumerate(translator.zip_translations())

        passages = [
            TranslatedPassage(hebrew, english, i + 1)
            for i, (hebrew, english) in translation_tuples
        ]

        data = TranslatedChapter(text_ref.section_num, text_ref.chapter_num, passages)

        # Writes data to the file
        data.to_file(file_path)
        print(f"Saved chapter to {file_path}")
        return (translator.chapter_num, True)
