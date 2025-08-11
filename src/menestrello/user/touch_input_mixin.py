from typing import ClassVar
import time
import board
import busio
import adafruit_mpr121

class TouchInputMixin:
    """
    Class to listen for touch events on the MPR121 capacitive touch sensor.
    Detects single tap, double tap, and long press.
    """
    SINGLE_TAP_MAX: ClassVar[float] = 0.3      # seconds
    DOUBLE_TAP_GAP_MAX: ClassVar[float] = 0.4  # seconds between taps
    LONG_PRESS_MIN: ClassVar[float] = 1.0      # seconds
    
    DEFAULT_MPR121_ADDRESS: ClassVar[int] = 0x5A       # Default I2C address for MPR121

    # EXIT: ClassVar[tuple[int,str]] = 
    START: ClassVar[tuple[int,str]] = (0, "long")
    UP: ClassVar[tuple[int,str]] = (0, "double")
    ONE: ClassVar[tuple[int,str]] = (1, "single")
    TWO: ClassVar[tuple[int,str]] = (2, "single")
    THREE: ClassVar[tuple[int,str]] = (3, "single")
    REPEAT: ClassVar[tuple[int,str]] = (0, "single")
    REPEAT_OPTIONS: ClassVar[tuple[int,str]] = (2, "single")
    EXIT: ClassVar[tuple[int,str]] = (11, "long")

    def __init__(self, i2c_bus=None, address=None):
        if i2c_bus is None:
            i2c_bus = busio.I2C(board.SCL, board.SDA)
        if address is None:
            address = self.DEFAULT_MPR121_ADDRESS
        self.mpr121 = adafruit_mpr121.MPR121(i2c_bus, address=address)

    def get_input(self):
        """
        Waits for a touch event and returns a tuple:
        (pin_number, event_type) where event_type is 'single', 'double', or 'long'
        """
        print("Touch any of the 12 MPR121 pins...")
        last_tap_time = {}
        tap_count = {}
        while True:
            # note that only the first 4 pins are used in this code
            for pin in range(0, 4):
                if self.mpr121[pin].value:
                    start_time = time.time()
                    # Wait until release
                    while self.mpr121[pin].value:
                        time.sleep(0.01)
                    duration = time.time() - start_time
                    # Long press
                    if duration >= self.LONG_PRESS_MIN:
                        return (pin, "long")

                    now = time.time()
                    # Double tap detection
                    if pin in last_tap_time and (now - last_tap_time[pin]) < self.DOUBLE_TAP_GAP_MAX:
                        tap_count[pin] += 1
                    else:
                        tap_count[pin] = 1
                    last_tap_time[pin] = now

                    # Double tap
                    if tap_count[pin] == 2:
                        tap_count[pin] = 0
                        return (pin, "double")
                    # Single tap
                    elif duration <= self.SINGLE_TAP_MAX:
                        # Wait briefly to see if a double tap follows
                        time.sleep(self.DOUBLE_TAP_GAP_MAX)
                        if tap_count[pin] == 1:
                            tap_count[pin] = 0
                            return (pin, "single")
            time.sleep(0.01)