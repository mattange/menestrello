from abc import ABC, abstractmethod
from typing import Any

from ..story.story_tree import StoryTree

class GenericUserIO(ABC):
    """
    Class to handle user input and output.
    """

    @abstractmethod
    def get_input(self) -> Any:
        pass

    @abstractmethod
    def provide_output(self, message: str | None = None, **kwargs) -> None:
        pass

    @abstractmethod
    def get_initial_story_prompt(self) -> str:
        pass

    @property
    def story(self) -> StoryTree | None:
        """
        The story that is being interacted with.
        """
        if hasattr(self, '_story'):
            return self._story # type: ignore
        return None
    
    @story.setter
    def story(self, s: StoryTree) -> None:
        """
        Set the story that is being interacted with.
        """
        self._story = s  # type: ignore