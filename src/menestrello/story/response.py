from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

from .option import Option

class Response(BaseModel):
    introduction: str | None = Field(None, description="A possible introduction by the chatbot.")
    title: str = Field(..., description="The title of the section.")
    fragment: str = Field(..., description="The content of the story section.")
    question: str | None = Field(None, description="The question for the user about the next section.")
    options: list[Option] | None = Field(None, description="The options for the user to choose from.", min_length=2, max_length=3)

    def tts_target(self, include_introduction=False, include_title=False) -> str:
        """
        Return the TTS target for the fragment.
        """
        s = ""
        if include_introduction and self.introduction:
            s += self.introduction + "\n\n"
        if include_title:
            s+= f"{self.title}\n\n"
        s += self.fragment + "\n\n"
        if self.question:
            s += f"{self.question}\n"
        if self.options:
            s += "\n".join([f"- {option.description}" for option in self.options]) + "\n\n"
        return s
