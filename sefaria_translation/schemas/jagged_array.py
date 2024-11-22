# jagget_array.py
from typing import (
    Union,
    List,
    Literal,
    TypedDict,
    Optional,
    Tuple,
    Annotated,
    TypeAlias,
)
from pydantic import BaseModel, Field, computed_field, model_validator
from sefaria_translation.schemas.sefaria_index import (
    SefariaTitleNode,
    SefariJaggedArrayNodeSchema,
)


def get_titles(
    titles: Optional[list[SefariaTitleNode]],
) -> Tuple[Optional[str], Optional[str]]:
    """Gets the primary hebrew and english title from Sefaria JSON data if they exist."""
    english: Optional[str] = None
    hebrew: Optional[str] = None
    if titles is not None:
        for t in titles:
            if t["primary"] == True and t["lang"] == "en":
                english = t["text"]
            if t["primary"] == True and t["lang"] == "he":
                hebrew = t["text"]
    return (english, hebrew)


# Our version of the schema
class JaggedArrayNodeSchema(BaseModel):
    depth: int
    section_names: list[str]
    content_block_title_english: Optional[str]
    content_block_title_hebrew: Optional[str]
    type: Literal["JaggedArrayNodeSchema"] = "JaggedArrayNodeSchema"

    @classmethod
    def from_json(cls, data: SefariJaggedArrayNodeSchema):
        titles: list[SefariaTitleNode] = data.get("titles")
        primary_titles: Tuple[Optional[str], Optional[str]] = (None, None)

        if titles is not None:
            primary_titles = get_titles(titles)
        """Converts Sefaria jagged node schema to our schema"""
        return cls(
            depth=data["depth"],
            section_names=data["sectionNames"],
            content_block_title_english=primary_titles[0],
            content_block_title_hebrew=primary_titles[1],
        )


# Define a non-recursive type for validation
# Type definition for up to 5 levels of depth
Depth1 = list[str]
Depth2 = list[Depth1]
Depth3 = list[Depth2]
Depth4 = list[Depth3]
Depth5 = list[Depth4]

FiniteDepthJaggedArray = Union[str, Depth1, Depth2, Depth3, Depth4, Depth5]

# class JaggedArrayType:
#     @classmethod
#     def validate(cls, v: Union[str, FiniteDepthArray]) -> Union[str, FiniteDepthArray]:
#         if isinstance(v, str):
#             return v
#         if isinstance(v, list):
#             return [cls.validate(item) for item in v]
#         raise ValueError(f"Expected string or list, got {type(v)}")


def validate_jagged_array(v: FiniteDepthJaggedArray) -> FiniteDepthJaggedArray:
    """Validates the jagged array structure"""
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return [validate_jagged_array(item) for item in v]
    raise ValueError(f"Expected string or list, got {type(v)}")


# Use Annotated to attach the validator
JaggedArray = Annotated[FiniteDepthJaggedArray, Field(validator=validate_jagged_array)]


def calculate_depth(arr: JaggedArray) -> int:
    if isinstance(arr, str):
        return 0
    if not arr:  # Empty list
        return 1
    return 1 + calculate_depth(arr[0])


class JaggedArrayNode(BaseModel):
    content: JaggedArray
    content_schema: JaggedArrayNodeSchema
    type: Literal["JaggedArrayNode"] = "JaggedArrayNode"

    @computed_field
    @property
    def depth(self) -> int:
        """Calculates the depth of the jagged array"""
        return calculate_depth(self.content)

    @model_validator(mode="after")
    def validate_section_names(self) -> "JaggedArrayNode":
        """Validates that number of section names matches depth"""
        if self.content_schema.depth != self.depth:
            raise ValueError(
                f"Content depth={self.depth} does not match schema depth={self.content_schema.depth}."
            )
        if len(self.content_schema.section_names) != self.depth:
            raise ValueError(
                f"Number of section names ({len(self.section_names)}) "
                f"must match depth ({self.depth})"
            )
        return self

    def get_section_name(self, depth_level: int) -> str:
        """
        Gets the section name for a specific depth level

        Args:
            depth_level: 1-based index of depth level

        Returns:
            Name of the section at that depth (e.g., "Gate", "Chapter", "Paragraph")
        """
        if not (1 <= depth_level <= self.depth):
            raise ValueError(
                f"Depth level must be between 1 and {self.primary_node.depth}"
            )
        return self.content_schema.section_names[depth_level - 1]


# Example usage:
if __name__ == "__main__":
    pass
