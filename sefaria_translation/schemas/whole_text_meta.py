from datetime import datetime
from typing import Literal
from sefaria_translation.schemas.jagged_array import JaggedArrayNodeSchema
from sefaria_translation.schemas.base_schema import BaseSchema
from sefaria_translation.sefaria_api.sefaria_index import SefariaIndex


class WholeTextMeta(BaseSchema):
    text_schema: list[JaggedArrayNodeSchema]
    title: str  # Display title
    sefaria_title: str  # underscored title for api calls, filenames, etc.
    sefaria_author_names: list[str]
    authors_display_names: str = (
        ""  # Provided manually since it does not appear to be in the index data.
    )

    type: Literal["WholeTextMeta"] = "WholeTextMeta"

    @classmethod
    def from_json(
        cls,
        data: SefariaIndex,
        authors_display_names: str = "",
        sefaria_title: str = "",
    ) -> "WholeTextMeta":

        if sefaria_title == "":
            sefaria_title = data["title"].replace(" ", "_")

        return cls(
            text_schema=[
                JaggedArrayNodeSchema.from_json(jag) for jag in data["schema"]["nodes"]
            ],
            title=data["title"],
            sefaria_title=sefaria_title,
            sefaria_author_names=data["authors"],
            authors_display_names=authors_display_names,
        )
