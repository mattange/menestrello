from typing import ClassVar

from .generic_user_interaction import GenericUserInteraction

class ConsoleUserInteraction(GenericUserInteraction):
    """
    Class to handle user input and output in the console.
    """
    EXIT_COMMAND: ClassVar[str] = "exit"
    RESET_COMMAND: ClassVar[str] = "reset"

    def get_input(self) -> str:
        """
        Get input from the user.
        """
        user_input = input("You: ").lower()
        return user_input

    def provide_output(self, message: str) -> None:
        """
        Provide output to the user.
        """
        print(f"Chatbot: {message}")