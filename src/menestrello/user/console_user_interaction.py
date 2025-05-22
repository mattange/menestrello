from typing import ClassVar

from .generic_user_interaction import GenericUserInteraction
from .text_user_interaction_mixin import TextUserInteractionMixin

class ConsoleUserInteraction(TextUserInteractionMixin, GenericUserInteraction):
    """
    Class to handle user input and output in the console.
    """
    EXIT: ClassVar[str] = "exit"
    RESET: ClassVar[str] = "reset"
    ONE: ClassVar[str] = "1"
    TWO: ClassVar[str] = "2"
    THREE: ClassVar[str] = "3"

    def get_input(self) -> str:
        """
        Get input from the user.
        """
        user_input = input("You: ").lower()
        return user_input
    
    def get_initial_story_prompt(self) -> str:
        return self.get_input()