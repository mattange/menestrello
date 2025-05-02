from pydantic import BaseModel

class StoryFragment(BaseModel):
    fragment_title: str
    fragment: str | None = None
    final_question: str | None = None
    future_options: list[str] | None = None
    fragment_audio_file_location: str | None = None
    choices_audio_file_location: str | None = None
    image_file_location: str | None = None
