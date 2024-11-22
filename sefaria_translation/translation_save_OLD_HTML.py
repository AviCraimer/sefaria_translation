# save_translation.py
from datetime import datetime
from pathlib import Path
from sefaria_translation.chapter_translator import TranslationState, ChapterTranslator
from typing import Literal, Optional, Union


def create_html_template(
    title: str, content: str, disclaimer: str, styles: str | None = None
) -> str:
    """
    Creates an HTML document from components
    """
    default_styles = """
        .passage { margin-bottom: 2em; }
        .hebrew { direction: rtl; margin-bottom: 1em; }
        footer { margin-top: 3em; font-size: 0.8em; color: #666; }
    """

    return f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            {styles or default_styles}
        </style>
    </head>
    <body>
        <main>
            <h3>{title}</h3>
            {content}
        </main>
        {disclaimer}
    </body>
    </html>
    """


OverwriteChoice = Literal["y", "n", "Y", "N"]


class SaveTranslation:
    BASE_DIR: Path = Path("saved_translations")
    _global_overwrite: Optional[Literal["Y", "N"]] = None

    def __init__(self, state: Union[TranslationState, ChapterTranslator]):
        self.translator = ChapterTranslator.from_state(state)
        # Create directory structure on initialization
        self.get_title_dir().mkdir(parents=True, exist_ok=True)

    def get_title_dir(self) -> Path:
        title: Path = self.translator.text_ref.title.lower()
        return self.BASE_DIR / title

    def get_save_path(self, filename: bool = True) -> Path:
        """
        Creates directory for saving a section.
        Returns either the directory path for the section, or the file path based on the `filename` argument.

        Examples:
        filename == True => "saved_translations/pardes_rimmonim/gate_6/pardes_rimmonim_6_3.html"
        filenames == False => "saved_translations/pardes_rimmonim/gate_6"
        """
        text_ref = self.translator.text_ref
        title_dir: Path = self.get_title_dir()

        # Strip any special characters that might cause issues in file paths
        chapter_dir: str = f"{text_ref.section_name}_{text_ref.section_num}"

        full_directory_path: Path = title_dir / chapter_dir

        # Create chapter-specific directory
        full_directory_path.mkdir(parents=True, exist_ok=True)

        file_name: str = ""
        if filename:
            file_name = text_ref.get_file_name() + ".html"
            return full_directory_path / file_name
        else:
            return full_directory_path

    def saved_exists(self) -> bool:
        file_path = self.get_save_path()
        return file_path.exists()

    def get_disclaimer(self) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"""
        <footer>
            <p>Disclaimer: The English text is translated by AI and may not be 100% accurate.
            The original Hebrew text was retrieved from
            <a href="https://sefaria.org" target="_blank">sefaria.org</a>
            on {today}.</p>
        </footer>
        """

    def format_translations(self) -> str:
        """Format translations as HTML"""
        translations = self.translator.get_translations()

        return "\n\n".join(
            f"<div class='passage'>\n"
            f"<div class='hebrew'>{hebrew}</div>\n"
            f"<div class='english'>{english}</div>\n"
            "</div>"
            for hebrew, english in translations
        )

    def prompt_overwrite(self, file_path: Path) -> OverwriteChoice:
        """
        Prompts user whether to overwrite existing file

        Returns:
            bool: True if file should be overwritten, False otherwise
        """
        # Check if we have a global choice
        if self.__class__._global_overwrite is not None:
            return self.__class__._global_overwrite

        while True:
            choice = input(
                f"\nFile already exists: {file_path}\n"
                "Overwrite? [y/n/Y/N] "
                "(y=yes, n=no, Y=yes to all, N=no to all): "
            )

            if choice not in ["y", "n", "Y", "N"]:
                print("Invalid choice. Please enter y, n, Y, or N")
                continue

            # Handle global choices
            if choice in ["Y", "N"]:
                self.__class__._global_overwrite = choice
            return choice

    def save_to_html(self) -> Path:
        """
        Saves translations to HTML file

        Returns:
            Path to saved file
        """

        # Check if file exists and prompt for overwrite
        file_path: Path = self.get_save_path()
        if file_path.exists() and self.prompt_overwrite(file_path).lower() == "n":
            print(f"Skipping existing: {file_path}")
            return file_path

        text_ref = self.translator.text_ref

        # Create HTML content
        title = text_ref.display_text(2)
        content = self.format_translations()
        disclaimer = self.get_disclaimer()

        html_content = create_html_template(
            title=title, content=content, disclaimer=disclaimer
        )

        # Save file
        file_path.write_text(html_content, encoding="utf-8")
        print(f"Saved HTML to {file_path}")

        return file_path
