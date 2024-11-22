# schemas.py
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from pathlib import Path


class BaseSchema(BaseModel):
    """Base class to use for all schemas with to add utility methods"""

    def to_file(self, file_path: Path) -> None:
        """Save data to JSON file"""
        file_path.write_text(self.model_dump_json(indent=2), encoding="utf-8")


class TranslatedPassage(BaseSchema):
    hebrew: str
    english: str
    passage_num: int
    type: Literal["TranslatedPassage"] = "TranslatedPassage"


# Each file will save a translated or untranslated chapter
class TranslatedChapter(BaseSchema):
    section_num: int
    chapter_num: int
    passages: list[TranslatedPassage]
    retrieved_at: datetime = Field(default_factory=datetime.now)
    translated_at: datetime = Field(default_factory=datetime.now)
    ai_model_version: str = "claude-3-sonnet-20240229"
    type: Literal["TranslatedChapter"] = "TranslatedChapter"

    @classmethod
    def from_file(cls, file_path: Path) -> "TranslatedChapter":
        """Load chapter from JSON file"""
        return cls.model_validate_json(file_path.read_text())


# The chapter content Will be written to files so we define meta-data in a root file.
# class SectionMeta(BaseSchema):
#     type: Literal["Section"]
#     section_num: int
#     number_of_chapters: int  # This lets us verify if all chapters have been translated
