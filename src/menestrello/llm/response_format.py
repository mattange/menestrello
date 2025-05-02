from pydantic import BaseModel

class InteractionResponseFormat(BaseModel):
    """Base class for interaction response formats."""
    content: str
    role: str = "assistant"
    story_title: str | None = None
    story_fragment: str | None = None
    question: str | None = None
    options: list[str] | None = None

    def __str__(self) -> str:
        """Return the string representation of the response."""
        s = ""
        if self.story_fragment:
            s += self.story_fragment
        if self.question:
            s = s + "\n" + self.question
        if self.options:
            s += "\n".join(self.options)

        return s
