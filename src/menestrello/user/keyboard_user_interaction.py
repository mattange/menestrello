from typing import ClassVar
from pynput import keyboard
import time

from .generic_user_interaction import GenericUserInteraction
from .text_user_interaction_mixin import TextUserInteractionMixin
from .keyboard_listener import KeyboardListener

class KeyboardUserInteraction(TextUserInteractionMixin, GenericUserInteraction):

    EXIT: ClassVar[keyboard.Key] = keyboard.Key.esc
    RESET: ClassVar[keyboard.Key] = keyboard.Key.backspace
    # OK: ClassVar[keyboard.Key] = keyboard.Key.enter
    # LEFT: ClassVar[keyboard.Key] = keyboard.Key.left
    # RIGHT: ClassVar[keyboard.Key] = keyboard.Key.right
    UP: ClassVar[keyboard.Key] = keyboard.Key.up
    # DOWN: ClassVar[keyboard.Key] = keyboard.Key.down
    ONE: ClassVar[keyboard.Key] = keyboard.Key.left
    TWO: ClassVar[keyboard.Key] = keyboard.Key.down
    THREE: ClassVar[keyboard.Key] = keyboard.Key.right
    REPEAT: ClassVar[keyboard.KeyCode] = keyboard.KeyCode.from_char('r')

    def __init__(self):
        super().__init__()
        keys_to_watch = {
            self.EXIT,
            self.RESET,
            self.UP,
            self.REPEAT,
            self.ONE,
            self.TWO,
            self.THREE,
        }
        self.keyboard_listener = KeyboardListener(keys_to_watch)
        self.keyboard_listener.start()

    def get_input(self) -> keyboard.Key:
        """
        Get input from the user.
        """
        print("Press 'esc' to exit, 'backspace' to reset, 'up' for up one level, 'r' to repeat, 'left' for 1, 'down' for 2, 'right' for 3.")
        pressed_keys = []
        while True:
            pressed_keys = self.keyboard_listener.get_pressed_keys()
            if pressed_keys:
                return pressed_keys[-1]
            time.sleep(0.1)

    def get_initial_story_prompt(self) -> str:
        user_input = input("Tell me the topic of the story: ").lower()
        return user_input
