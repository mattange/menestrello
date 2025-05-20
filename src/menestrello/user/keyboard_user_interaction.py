from typing import ClassVar
from pynput import keyboard

from .generic_user_interaction import GenericUserInteraction
from .text_user_interaction_mixin import TextUserInteractionMixin
from .keyboard_listener import KeyboardListener

class KeyboardUserInteraction(TextUserInteractionMixin, GenericUserInteraction):

    EXIT_COMMAND: ClassVar[keyboard.Key] = keyboard.Key.esc
    RESET_COMMAND: ClassVar[keyboard.Key] = keyboard.Key.up
    PREVIOUS_COMMAND: ClassVar[keyboard.Key] = keyboard.Key.left
    NEXT_COMMAND: ClassVar[keyboard.Key] = keyboard.Key.right
    OK_COMMAND: ClassVar[keyboard.Key] = keyboard.Key.enter

    def __init__(self):
        super().__init__()
        self.keyboard_listener = KeyboardListener()

    def get_input(self) -> str:
        """
        Get input from the user.
        """
        print("Press 'esc' to exit, 'up' to reset, 'left' for previous, 'right' for next, or 'enter' to confirm.")
        self.keyboard_listener.start()
        pressed_keys = []
        while self.keyboard_listener.is_running():
            pressed_keys = self.keyboard_listener.get_pressed_keys()
            if pressed_keys:
                self.keyboard_listener.stop()
        return pressed_keys[-1]

    def get_initial_story_prompt(self) -> str:
        user_input = input("Tell me the topic of the story: ").lower()
        return user_input
