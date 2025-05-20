from pynput import keyboard
import threading

class KeyboardListener:
    def __init__(self):
        # Watch for arrow keys, enter, and escape
        self.keys_to_watch = {
            keyboard.Key.left,
            keyboard.Key.right,
            keyboard.Key.down,
            keyboard.Key.up,
            keyboard.Key.enter,
            keyboard.Key.esc,
        }
        self.pressed_keys = set()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self._lock = threading.Lock()
        self._running = False

    def on_press(self, key):
        if key in self.keys_to_watch:
            with self._lock:
                self.pressed_keys.add(key)

    def start(self):
        self._running = True
        self.listener.start()

    def stop(self):
        self._running = False
        self.listener.stop()

    def get_pressed_keys(self):
        with self._lock:
            keys = list(self.pressed_keys)
            self.pressed_keys.clear()
        return keys
    
    def is_running(self):
        return self._running

# Example usage:
# listener = SpecialKeyListener()
# listener.start()
# while True:
#     pressed = listener.get_pressed_keys()
#     if pressed:
#         print("Pressed:", pressed)
#     # ... rest of your loop code ...