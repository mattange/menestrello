from abc import ABC, abstractmethod
from typing import Any

class GenericUserInteraction(ABC):
    """
    Class to handle user input and output.
    """

    @abstractmethod
    def get_input(self) -> Any:
        pass

    @abstractmethod
    def provide_output(self, message: str) -> None:
        pass

    @abstractmethod
    def get_initial_story_prompt(self) -> str:
        pass