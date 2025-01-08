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


# TODO: Write a function that takes a WholeTextMeta and creates a directory structure
#   / sefaria_translation_library
#     / Kabbalah
#       /pardes_rimmonim
#         _meta_of__pardes_rimmonim.json
#       /content   (No files directly in this folder)
#          /01_authors_introduction
#              _meta_of__authors_introduction.json
#          /02_index (depth=2, gates and chapters)
#              _meta_of__index.json
#          /03_a_prayer
#              _meta_of__a_prayer
#          /04_content_block    # No title is provided
#              _ meta_of__content_block_04.json
#              /01_gate
#                   _meta_of__gate_01.json
#              /02_gate
#                   _meta_of__gate_02.json  # These will the same, but it's worth duplicating I guess.


# With translation json files later
#
#  /pardes_rimmonim
#    text_meta.json
#     /content
# -- /01_authors_introduction
#   --  01_paragraph.json
# -- /02_index (depth=2, gates and chapters)
#   -- 01_gate.json
#   -- 02_gate.json
#     .. etc
# -- /03_a prayer
#   -- 01_paragraph.json
# -- /04_main_text
#   -- /01_gate
#     -- 01_chapter.json
#     -- 02_chapter.json
#   -- /02_gate
#     -- 01_chapter.json
#     -- 02_chapter.json

# -- Move to sefaria_api folder

# --
