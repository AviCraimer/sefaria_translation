# save_translation.test.py
import pytest
from pathlib import Path
from datetime import datetime
from sefaria_translation.schemas.base_schema import WholeTextMeta, SectionMeta
from sefaria_translation.save_translation import SaveTranslation
from sefaria_translation.text_reference import TextReference


# Sample test data
@pytest.fixture
def sample_meta():
    return WholeTextMeta(
        type="WholeTextMeta",
        sections_meta=[
            SectionMeta(type="Section", section_num=1, number_of_chapters=3),
            SectionMeta(type="Section", section_num=2, number_of_chapters=4),
        ],
        title="Pardes Rimmonim",
        sefaria_title="Pardes_Rimmonim",
        author_full_name="Moses ben Jacob Cordovero",
        author_last_name="Cordovero",
    )


@pytest.fixture
def saver(sample_meta):
    return SaveTranslation(sample_meta)


def test_path_generation(saver):
    """Test path generation methods"""
    # Test whole text path
    assert saver.get_whole_text_path == Path("saved_translations/pardes_rimmonim")

    # Test metadata file path
    assert saver.get_meta_file_path == Path(
        "saved_translations/pardes_rimmonim/metadata_pardes_rimmonim.json"
    )

    # Test section path
    assert saver.get_section_path(1) == Path(
        "saved_translations/pardes_rimmonim/section_001"
    )
    assert saver.get_section_path(10) == Path(
        "saved_translations/pardes_rimmonim/section_010"
    )


def test_chapter_file_path(saver):
    """Test chapter file path generation"""
    ref = TextReference(title="Pardes_Rimmonim", section_num=6, chapter_num=3)
    expected = Path(
        "saved_translations/pardes_rimmonim/section_006/pardes_rimmonim_006_003.json"
    )
    assert saver.get_chapter_file_path(ref) == expected


def test_chapter_file_path_validation(saver):
    """Test that chapter file path raises error when chapter number is missing"""
    ref = TextReference(
        title="Pardes_Rimmonim",
        section_num=6,
    )
    with pytest.raises(ValueError, match="Chapter Number is undefiend"):
        saver.get_chapter_file_path(ref)


# You might also want to test the path structure creation
def test_section_paths_created(sample_meta, tmp_path):
    """Test that section directories are created correctly"""
    # Temporarily override BASE_DIR
    SaveTranslation.BASE_DIR = tmp_path
    saver = SaveTranslation(sample_meta)

    # Check that directories were created
    assert (tmp_path / "pardes_rimmonim").exists()
    assert (tmp_path / "pardes_rimmonim" / "section_001").exists()
    assert (tmp_path / "pardes_rimmonim" / "section_002").exists()

    # Check that metadata file was created
    meta_file = tmp_path / "pardes_rimmonim" / "metadata_pardes_rimmonim.json"
    assert meta_file.exists()
