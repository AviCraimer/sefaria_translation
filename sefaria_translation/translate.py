# translator.py
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic
from typing import Iterator
from sefaria_api import format_text
from text_reference import TextReference, ReferenceLevel
from translation_prompt import translation_prompt
from secret import anthropic_api_key

client = Anthropic(api_key=anthropic_api_key)


def ask_claude(prompt: str) -> str:
    return (
        client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-5-sonnet-latest",
        )
        .content[0]
        .text
    )


print(ask_claude("Hi there, are you fishing?"))


class ChapterTranslator:
    def __init__(self, text_ref: TextReference, chapter: list[str]) -> None:
        self.text_ref = text_ref
        self.text_ref.passage_num = 1
        self.chapter = chapter

    def translate_passage(self) -> str:
        """Translate a single passage with full chapter context"""
        prompt = translation_prompt(self.text_ref, self.chapter)

        response = ask_claude(prompt)
        return response

    # def translate_chapter(
    #     self, text_array: list[str], title: str, section_num: int, chapter_num: int
    # ) -> Iterator[str]:
    #     """
    #     Translates each passage in the chapter, yielding results one at a time
    #     """
    #     # Get full chapter context
    #     context = format_text(text_array)

    #     # Translate each passage
    #     for passage in text_array:
    #         if passage.strip():  # Skip empty passages
    #             translation = self.translate_passage(
    #                 passage, context, title, section_num, chapter_num
    #             )
    #             yield translation
