# translate.py
from ast import Pass
from sefaria_translation.text_reference import (
    TextReference,
    ChapterReference,
    PassageReference,
)
from sefaria_translation.translation_prompt import translation_prompt
from sefaria_translation.claude import ask_claude
from typing import Optional, Callable


class ChapterTranslator:
    def __init__(
        self,
        chapter_ref: ChapterReference,
        chapter: list[str],
        llm_generation: Callable[[str], str] = ask_claude,
    ) -> None:
        if not chapter:
            raise ValueError("Chapter cannot be empty")

        self.chapter_ref: ChapterReference = chapter_ref
        self.chapter: list[str] = chapter
        self.llm_generation = llm_generation
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

    @classmethod
    def clone(Cls, state: "ChapterTranslator") -> "ChapterTranslator":
        """Gets new chapter translator from an existing chapter translator"""
        translator = Cls(state.chapter_ref, state.chapter)
        translator.translations = state.translations
        return translator

    def translate_passage(self) -> Optional[str]:
        """Translate a single passage with full chapter context"""
        self.chapter_ref.passage_num = self.next_passage_num
        if self.chapter_ref.passage_num is None:
            # Translation is complete
            return None
        passage_ref = PassageReference.from_ref(self.chapter_ref)
        prompt = translation_prompt(passage_ref, self.chapter)
        response = self.llm_generation(prompt)
        self.translations.append(response)
        return response

    def zip_translations(self) -> list[tuple[str, str]]:
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
                    print(
                        f"Translation of {self.chapter_ref.display_text(2)} complete."
                    )
                    break
                print(f"Passage {len(self.translations)} translated.")
            return self.zip_translations()
        except Exception as e:
            error_message = str(e).lower()
            # TODO: This is Anthropic specific, in future I may want to make the error handling use dependency injection, but for now this is ok.
            if (
                "overloaded_error" in error_message
                or "error code: 529" in error_message
            ):
                raise Exception("Anthropic server is busy, try again later.") from e
            else:
                # Include partial translations in the error
                completed_translations = self.zip_translations()
                raise Exception(
                    f"Translation failed at passage {self.next_passage_num}."
                    f"Completed {len(completed_translations)}/{len(self.chapter)} passages. "
                    f"Error: {str(e)}"
                ) from e
