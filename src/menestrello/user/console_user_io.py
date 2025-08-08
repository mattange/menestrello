from typing import ClassVar

from .generic_user_io import GenericUserIO
from .text_output_mixin import TextOutputMixin

class ConsoleUserIO(TextOutputMixin, GenericUserIO):
    """
    Class to handle user input and output in the console.
    """
    EXIT: ClassVar[str] = "exit"
    RESET: ClassVar[str] = "reset"
    UP: ClassVar[str] = "up"
    ONE: ClassVar[str] = "1"
    TWO: ClassVar[str] = "2"
    THREE: ClassVar[str] = "3"
    REPEAT: ClassVar[str] = "repeat"

    def get_input(self) -> str:
        """
        Get input from the user.
        """
        print("Type 'exit' to end the conversation, 'reset' to reset, 'up' to go up one level, '1', '2', or '3' for options, or 'repeat' to repeat the last options.")
        user_input = input("You: ").lower()
        return user_input