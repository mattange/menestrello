from abc import ABC, abstractmethod
from typing import Any, ClassVar

class GenericUserInteraction(ABC):
    """
    Class to handle user input and output.
    """

    EXIT_COMMAND: ClassVar[Any] = None
    RESET_COMMAND: ClassVar[Any] = None

    @abstractmethod
    def get_input(self) -> Any:
        pass

    @abstractmethod
    def provide_output(self, message: str) -> None:
        pass