from sefaria_translation.sefaria_api.fetch_sefaria_text import format_text
from sefaria_translation.text_reference import PassageReference


def translation_prompt(text_ref: PassageReference, chapter: list[str]) -> str:
    """
    Creates a translation prompt for a specific passage within its chapter context

    Args:
        text_ref: Reference containing section, chapter, and passage information
        chapter: List of passages in the chapter

    Raises:
        ValueError: If passage number is missing or invalid
    """
    if text_ref.passage_num is None:
        raise ValueError("Passage number must be provided")
    passage_index = text_ref.passage_num - 1
    if passage_index < 0 or passage_index >= len(chapter):
        raise ValueError("Passage is not in chapter list")

    # Add XML tags to target passage
    marked_chapter = chapter.copy()
    marked_chapter[passage_index] = (
        f"<passage-to-translate>{marked_chapter[passage_index]}</passage-to-translate>"
    )
    return f"""<system>You are translating Hebrew religious texts into English.</system>

Context for this translation (text information and the full chapter in which the passage appears).

<text-information>
{text_ref.display_text()}
</text-information>

<context>
{format_text(marked_chapter)}
</context>

Please translate the following specific passage from this chapter:

{marked_chapter[passage_index]}

<guidelines>
- Maintain a scholarly tone
- Translate for clarity while preserving meaning
- Preserve any html tags that may be present in the hebrew text
- Do not output anything else before or after the translation.
</guidelines>

Please begin your translation:\n\n
"""


# Old stuff
# - Include any necessary contextual clarifications of meaning which are not in the original Hewbrew within [square brackets]
