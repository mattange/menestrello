
class TextOutputMixin:
    
    def provide_output(self, message: str | None = None, **kwargs) -> None:
        """
        Provide output to the user.
        """
        if message is not None:
            print(message)

    def present_introduction(self) -> None:
        """
        Present the introduction to the user.
        """
        print("Welcome to the Interactive Storytelling Chatbot!")
        print("You can interact with the chatbot by typing your responses or using keyboard shortcuts.")

    def goodbye(self) -> None:
        """
        Provide a goodbye message to the user.
        """
        print("Goodbye! Thank you for using the Interactive Storytelling Chatbot.")
