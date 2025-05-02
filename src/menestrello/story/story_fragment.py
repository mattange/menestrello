from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class StoryFragment:
    title: str
    fragment: str
    question: str | None = None
    options: list[str] | None = None
    # These fields are set to None by default and are not included in the constructor
    audio_file_path: str | None = Field(default=None, init=False)
    choices_audio_file_path: str | None = Field(default=None, init=False)
    image_file_path: str | None = Field(default=None, init=False)

    @classmethod
    def from_json(cls, json_data: dict) -> "StoryFragment":
        """
        Create a StoryFragment instance from a JSON object.
        """
        return cls(
            title=json_data.get("title", ""),
            fragment=json_data.get("fragment", ""),
            question=json_data.get("question"),
            options=json_data.get("options"),
        )
    
    def tts_target(self, include_title=False) -> str:
        """
        Return the TTS target for the fragment.
        """
        if include_title:
            s = f"{self.title}\n"
        else:
            s = ""
        s += self.fragment
        if self.question:
            s += f"\n{self.question}\n"
        if self.options:
            s += "\n".join([f"{i + 1}. {option}" for i, option in enumerate(self.options)])
        return s
    