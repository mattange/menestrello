from typing import ClassVar
from pynput import keyboard
import time

from .keyboard_listener import KeyboardListener

class KeyboardInputMixin():

    EXIT: ClassVar[keyboard.Key] = keyboard.Key.esc
    START: ClassVar[keyboard.Key] = keyboard.Key.backspace
    UP: ClassVar[keyboard.Key] = keyboard.Key.up
    ONE: ClassVar[keyboard.Key] = keyboard.Key.left
    TWO: ClassVar[keyboard.Key] = keyboard.Key.down
    THREE: ClassVar[keyboard.Key] = keyboard.Key.right
    REPEAT: ClassVar[keyboard.KeyCode] = keyboard.KeyCode.from_char('r')

    def __init__(self):
        super().__init__()
        keys_to_watch = {
            self.EXIT,
            self.START,
            self.UP,
            self.REPEAT,
            self.ONE,
            self.TWO,
            self.THREE,
        }
        self.keyboard_listener = KeyboardListener(keys_to_watch)
        

    def get_input(self) -> keyboard.Key:
        """
        Get input from the user.
        """
        print("Press 'ESC' to exit, 'BKSP' to start, 'UP' for up one level, 'R' to repeat, 'LEFT' for 1, 'DOWN' for 2, 'RIGHT' for 3.")
        pressed_keys = []
        if not self.keyboard_listener.is_running():
            self.keyboard_listener.start()
        while True:
            pressed_keys = self.keyboard_listener.get_pressed_keys()
            if pressed_keys:
                self.keyboard_listener.stop()
                return pressed_keys[-1]
            time.sleep(0.1)
