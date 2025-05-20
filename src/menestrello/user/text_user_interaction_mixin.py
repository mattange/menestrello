
class TextUserInteractionMixin:
    
    def provide_output(self, message: str) -> None:
        """
        Provide output to the user.
        """
        print(message)

    def present_introduction(self) -> None:
        """
        Present the introduction to the user.
        """
        print("'exit' to end the conversation.")
        print("'reset' to reset the conversation.")
        print("'1' for first option, '2' for second and so on.")

    def goodbye(self) -> None:
        """
        Provide a goodbye message to the user.
        """
        print("Goodbye! Thank you for using the Interactive Storytelling Chatbot.")

