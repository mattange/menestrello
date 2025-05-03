from pydantic.dataclasses import dataclass
from pydantic import Field
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class StoryFragment:
    title: str
    fragment: str
    question: str | None = None
    options: list[dict[str,int | str]] | None = None
    introduction: str | None = None
    # These fields are set to None by default and are not included in the constructor
    raw_json_string: str | None = Field(default=None, init=False)
    audio_file_path: str | None = Field(default=None, init=False)
    choices_audio_file_path: str | None = Field(default=None, init=False)
    image_file_path: str | None = Field(default=None, init=False)

    @classmethod
    def from_json_string(cls, json_string: str) -> "StoryFragment":
        """
        Create a StoryFragment instance from a JSON object.
        """
        json_data = json.loads(json_string)

        c = cls(
            title=json_data.get("title", ""),
            fragment=json_data.get("fragment", ""),
            question=json_data.get("question"),
            options=json_data.get("options"),
            introduction=json_data.get("introduction"),
        )
        c.raw_json_string = json_string
        return c
    
    def tts_target(self, include_introduction=False, include_title=False) -> str:
        """
        Return the TTS target for the fragment.
        """
        s = ""
        if include_introduction and self.introduction:
            s += self.introduction + "\n"
        if include_title:
            s+= f"{self.title}\n"
        s += self.fragment + "\n"
        if self.question:
            s += f"{self.question}\n"
        if self.options:
            s += "\n".join([f"{option["number"]}. {option["description"]}" for option in self.options]) + "\n"
        return s
    