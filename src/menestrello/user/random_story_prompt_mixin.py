from pathlib import Path
import random

current_dir = Path(__file__).resolve().parent
statics_dir = current_dir / "random_story_mixin_static"

class RandomStoryPromptMixin:
    """
    Mixin class to provide random story prompt generation functionality.
    """
    def _read_lines_from_file(self, filepath: str | Path) -> list[str]:
        # Reads lines from a text file and returns them as a list of strings
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.rstrip('\n') for line in f]

    def get_initial_story_prompt(self) -> str:

        available_story_characters = self._read_lines_from_file(statics_dir / "available_story_characters.txt")
        available_story_settings = self._read_lines_from_file(statics_dir / "available_story_settings.txt")
        user_input = (
            "Tell me a story about " 
            + available_story_characters[random.randint(0, len(available_story_characters) - 1)]
            + available_story_settings[random.randint(0, len(available_story_settings) - 1)]
        )
        return user_input

