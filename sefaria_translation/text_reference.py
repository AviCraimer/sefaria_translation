from dataclasses import dataclass, field
from typing import Optional, Literal, Union, TypeVar

ReferenceLevel = Literal[1, 2, 3]

T = TypeVar("T", bound="TextReference")


@dataclass
class TextReference:
    title: str
    section_num: int
    chapter_num: Optional[int] = None
    passage_num: Optional[int] = None

    # Custom names for the parts
    section_name: str = "Section"
    chapter_name: str = "Chapter"
    passage_name: str = "Passage"
    _valid_levels: list[ReferenceLevel] = field(default_factory=lambda: [1, 2, 3])

    def __post_init__(self) -> None:
        """Validate after initialization"""
        if not self.title:
            raise ValueError("Title cannot be empty")
        if self.section_num < 1:
            raise ValueError("Section number must be positive")
        if self.chapter_num is not None and self.chapter_num < 1:
            raise ValueError("Chapter number must be positive")
        if self.passage_num is not None and self.passage_num < 1:
            raise ValueError("Passage number must be positive")

    @property
    def ref_level(self) -> ReferenceLevel:
        count: ReferenceLevel = 1
        if self.chapter_num is not None:
            count = 2
        if self.chapter_num is not None and self.passage_num is not None:
            count = 3
        return count

    @property
    def has_valid_level(self) -> bool:
        return self.ref_level in self._valid_levels

    @classmethod
    def from_ref(
        cls: type[T],
        ref: Union["TextReference", "ChapterReference", "PassageReference"],
    ) -> T:
        """Create reference from reference."""
        try:
            new_ref = cls(
                title=ref.title,
                section_num=ref.section_num,
                chapter_num=ref.chapter_num,
                passage_num=ref.passage_num,
                section_name=ref.section_name,
                chapter_name=ref.chapter_name,
                passage_name=ref.passage_name,
            )
        except:
            level_name = cls.__name__.split("Reference")[0].lower()
            raise ValueError(
                f"Cannot create {cls.__name__}, {level_name} number is missing"
            )
        return new_ref

    def display_text(
        # TODO: Add author to text reference
        self,
        level: ReferenceLevel | Literal[0] = 0,
        include_title: bool = True,
        include_author: bool = False,
    ) -> str:
        """
        Renders reference as human-readable text
        Example: "Pardes Rimmonim, Gate 6, Chapter 5, Passage 3"
        """
        parts = []
        if level == 0:
            level = self.ref_level
        if include_title:
            parts.append(self.title.replace("_", " "))

        parts.append(f"{self.section_name} {self.section_num}")

        if level >= 2:
            if self.chapter_num is None:
                raise ValueError(
                    f"Level set to {level} but no {self.chapter_name} number"
                )
            parts.append(f"{self.chapter_name} {self.chapter_num}")

        if level == 3:
            if self.passage_num is None:
                raise ValueError(
                    f"Level set to {level} but no {self.passage_name} number."
                )
            parts.append(f"{self.passage_name} {self.passage_num}")

        return ", ".join(parts)

    def to_url_path(self, level: ReferenceLevel = 1) -> str:
        """
        Converts reference to URL path format with specified depth

        Args:
            level: 1 for section only, 2 for section+chapter, 3 for section+chapter+passage

        Returns:
            URL path string (e.g., "Title_6_5_3")
        """
        if level < 1 or level > 3:
            raise ValueError("Level must be between 1 and 3")

        parts = [self.title, str(self.section_num)]

        if level >= 2:
            if self.chapter_num is None:
                raise ValueError("Chapter number required for level 2 or 3")
            parts.append(str(self.chapter_num))

        if level == 3:
            if self.passage_num is None:
                raise ValueError("Passage number required for level 3")
            parts.append(str(self.passage_num))

        return "_".join(parts)

    def get_file_name(self, level: ReferenceLevel = 2) -> str:
        """
        Creates a snake_case filename (without extension) based on reference

        Example: "pardes_rimmonim_6_5"
        """
        parts = [self.title.lower()]

        parts.append(str(self.section_num))

        if level >= 2 and self.chapter_num is not None:
            parts.append(str(self.chapter_num))

        if level >= 3 and self.passage_num is not None:
            parts.append(str(self.passage_num))

        return "_".join(parts)


@dataclass
class ChapterReference(TextReference):
    chapter_num: int  # Override to make it required (non-Optional)
    _valid_levels: list[ReferenceLevel] = field(default_factory=lambda: [2, 3])

    def __post_init__(self) -> None:
        """Stricter validation for chapter reference"""
        if not self.has_valid_level:
            raise ValueError(
                f"Reference Level is invalid for {self.__class__.__name__}"
            )


@dataclass
class PassageReference(ChapterReference):
    passage_num: int  # Override to make it required
    _valid_levels: list[ReferenceLevel] = field(default_factory=lambda: [3])


# Usage examples:
if __name__ == "__main__":
    # Basic usage
    ref = TextReference("Pardes_Rimmonim", 6, 5, 3)
    print(ref.display_text())  # "Pardes Rimmonim, Section 6, Chapter 5, Passage 3"

    # Custom section names
    gate_ref = TextReference(
        title="Pardes_Rimmonim",
        section_num=6,
        chapter_num=5,
        section_name="Gate",
        chapter_name="Portal",
    )

    gate_chapter_ref = ChapterReference.from_ref(gate_ref)  # Typed As Chapter Ref
    # gate_passage_ref = PassageReference.from_ref(gate_ref)  # Should through error

    print(gate_ref.display_text())  # "Pardes Rimmonim, Gate 6, Portal 5"
    print(gate_ref.display_text(1))  # "Pardes Rimmonim, Gate 6"

    # To avoid typing all the named arguments, can set it like this:
    gate_ref2 = TextReference("Pardes_Rimmonim", 6, 5, 3)
    gate_ref2.section_name = "Gate"
    print(gate_ref2.display_text())  # Pardes Rimmonim, Gate 6, Chapter 5, Passage 3
    print(gate_ref2.display_text(2))  # Pardes Rimmonim, Gate 6, Chapter 5

    # URL paths at different levels
    # print(gate_ref.to_url_path(1))  # "Pardes_Rimmonim_6"
    # print(gate_ref.to_url_path(2))  # "Pardes_Rimmonim_6_5"

    # Section-only reference
    section_ref = TextReference("Some_Text", 3)
    # print(section_ref.display_text())  # "Some Text, Section 3"
