from typing import ClassVar

from .generic_user_interaction import GenericUserInteraction
from .text_user_interaction_mixin import TextUserInteractionMixin

class ConsoleUserInteraction(TextUserInteractionMixin, GenericUserInteraction):
    """
    Class to handle user input and output in the console.
    """
    EXIT_COMMAND: ClassVar[str] = "exit"
    RESET_COMMAND: ClassVar[str] = "reset"
    PREVIOUS_COMMAND: ClassVar[str] = "1"
    NEXT_COMMAND: ClassVar[str] = "3"
    OK_COMMAND: ClassVar[str] = "2"

    def get_input(self) -> str:
        """
        Get input from the user.
        """
        user_input = input("You: ").lower()
        return user_input
    
    def get_initial_story_prompt(self) -> str:
        return self.get_input()