from typing import Literal, Optional, TypedDict


class SefariaTitleNode(TypedDict):
    """Title node json from the Sefaria API"""

    lang: Literal["en", "he"]
    text: str
    primary: bool


class SefariJaggedArrayNodeSchema(TypedDict):
    depth: int
    sectionNames: list[str]
    titles: Optional[list[SefariaTitleNode]]
    nodeType: Literal["JaggedArrayNode"] = "JaggedArrayNode"


class SefariaIndexSchema(TypedDict):
    nodes: list[SefariJaggedArrayNodeSchema]
    titles: Literal["todo"]


class SefariaIndex(TypedDict):
    title: str
    schema: SefariaIndexSchema
    categories: list[str]
    enDesc: str  # Description
    authors: list[str]
    default_struct: str  # Not sure if this is useful
