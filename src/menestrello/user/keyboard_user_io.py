from typing import ClassVar
from pynput import keyboard
import time

from .generic_user_io import GenericUserIO
from .text_output_mixin import TextOutputMixin
from .keyboard_listener import KeyboardListener

class KeyboardUserIO(TextOutputMixin, GenericUserIO):

    EXIT: ClassVar[keyboard.Key] = keyboard.Key.esc
    RESET: ClassVar[keyboard.Key] = keyboard.Key.backspace
    UP: ClassVar[keyboard.Key] = keyboard.Key.up
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
        print("Press 'ESC' to exit, 'BKSP' to reset, 'UP' for up one level, 'R' to repeat, 'LEFT' for 1, 'DOWN' for 2, 'RIGHT' for 3.")
        pressed_keys = []
        while True:
            pressed_keys = self.keyboard_listener.get_pressed_keys()
            if pressed_keys:
                return pressed_keys[-1]
            time.sleep(0.1)
