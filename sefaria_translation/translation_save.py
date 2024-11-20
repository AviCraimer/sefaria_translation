# save_translation.py
from datetime import datetime
from pathlib import Path
from translate import TranslationState, ChapterTranslator


class SaveTranslation:
    def __init__(self, state: TranslationState):
        self.translation = ChapterTranslator.from_state(state)

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
        translations = self.translation.get_translations()

        return "\n\n".join(
            f"<div class='passage'>\n"
            f"<div class='hebrew'>{hebrew}</div>\n"
            f"<div class='english'>{english}</div>\n"
            "</div>"
            for hebrew, english in translations
        )

    def save_to_html(self) -> str:
        """
        Saves translations to HTML file

        Returns:
            Path to saved file
        """
        # Create directory if it doesn't exist
        dir_name = self.translation.text_ref.title.lower()
        Path(dir_name).mkdir(exist_ok=True)

        # Generate filename
        base_name = self.translation.text_ref.get_file_name()
        file_path = f"{dir_name}/{base_name}.html"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{self.translation.text_ref.display_text(2)}</title>
            <style>
                .passage {{ margin-bottom: 2em; }}
                .hebrew {{ direction: rtl; margin-bottom: 1em; }}
                footer {{ margin-top: 3em; font-size: 0.8em; color: #666; }}
            </style>
        </head>
        <body>
            <h3>{self.translation.text_ref.display_text(2, include_title=False)}</h3>

            {self.format_translations()}

            {self.get_disclaimer()}
        </body>
        </html>
        """

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved HTML to {file_path}")

        return file_path


# Usage example:
if __name__ == "__main__":
    # Assuming you have a translation state
    state = TranslationState(...)
    saver = SaveTranslation(state)
    file_path = saver.save_to_html()
    print(f"Saved translations to {file_path}")
