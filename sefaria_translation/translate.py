# translate.py
from numpy import isin
from text_reference import TextReference, ReferenceLevel
from translation_prompt import translation_prompt
from claude import ask_claude
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranslationState:
    text_ref: TextReference
    chapter: list[str]
    translations: list[str]


class ChapterTranslator:
    def __init__(self, text_ref: TextReference, chapter: list[str]) -> None:
        if not chapter:
            raise ValueError("Chapter cannot be empty")
        if text_ref.chapter_num is None:
            raise ValueError("Chapter number must be specified in text_ref")

        self.text_ref: TextReference = text_ref
        self.chapter: list[str] = chapter
        self.translations: list[str] = []

    @property
    def is_complete(self) -> bool:
        return len(self.translations) == len(self.chapter)

    @property
    def next_passage_num(self) -> Optional[int]:
        """
        Returns the 1-based index of the next passage to translate, or None if complete
        Note: Passage numbers are 1-based to match traditional text references
        """
        if self.is_complete:
            return None
        if len(self.translations) > len(self.chapter):
            raise ValueError(
                "Something is wrong, more translations than passages in chapter."
            )
        zero_based_index = len(self.translations)
        return zero_based_index + 1  # Convert to 1-based passage number

    def save_state(self) -> TranslationState:
        return TranslationState(
            text_ref=self.text_ref, chapter=self.chapter, translations=self.translations
        )

    @classmethod
    def from_state(
        Cls, state: TranslationState | "ChapterTranslator"
    ) -> "ChapterTranslator":
        """Gets new chapter translator from translation state or an existing chapter translator"""
        translator = Cls(state.text_ref, state.chapter)
        translator.translations = state.translations
        return translator

    def translate_passage(self) -> Optional[str]:
        """Translate a single passage with full chapter context"""
        self.text_ref.passage_num = self.next_passage_num
        if self.text_ref.passage_num is None:
            # Translation is complete
            return None
        prompt = translation_prompt(self.text_ref, self.chapter)
        response = ask_claude(prompt)
        self.translations.append(response)
        return response

    def get_translations(self) -> list[tuple[str, str]]:
        """Returns list of (original, translation) pairs for completed translations"""
        return list(zip(self.chapter[: len(self.translations)], self.translations))

    def translate_chapter(self) -> list[tuple[str, str]]:
        """
        Translates all remaining passages in the chapter

        Returns:
            List of (original, translation) pairs for the entire chapter
        """
        try:
            while not self.is_complete:
                translation = self.translate_passage()
                if translation is None:
                    print(f"Translation of {self.text_ref.display_text(2)} complete.")
                    break
                print(f"Passage {len(self.translations)} translated.")
            return self.get_translations()
        except Exception as e:
            error_message = str(e).lower()
            if (
                "overloaded_error" in error_message
                or "error code: 529" in error_message
            ):
                raise Exception("Anthropic server is busy, try again later.") from e
            else:
                # Include partial translations in the error
                completed_translations = self.get_translations()
                raise Exception(
                    f"Translation failed at passage {self.next_passage_num}."
                    f"Completed {len(completed_translations)}/{len(self.chapter)} passages. "
                    f"Error: {str(e)}"
                ) from e
