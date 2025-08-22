from typing import ClassVar
import time
import board # pyright: ignore[reportMissingImports]
import busio # pyright: ignore[reportMissingImports]
import adafruit_mpr121 # pyright: ignore[reportMissingImports]

class TouchInputMixin:
    """
    Class to listen for touch events on the MPR121 capacitive touch sensor.
    Detects single tap, double tap, and long press.
    """
    SINGLE_TAP_MAX: ClassVar[float] = 0.3      # seconds
    DOUBLE_TAP_GAP_MAX: ClassVar[float] = 0.4  # max seconds between taps
    LONG_PRESS_MIN: ClassVar[float] = 1.0      # seconds
    
    DEFAULT_MPR121_ADDRESS: ClassVar[int] = 0x5A       # Default I2C address for MPR121

    # EXIT: ClassVar[tuple[int,str]] = 
    START: ClassVar[tuple[int,str]] = (0, "long")
    UP: ClassVar[tuple[int,str]] = (0, "double")
    ONE: ClassVar[tuple[int,str]] = (1, "single")
    TWO: ClassVar[tuple[int,str]] = (2, "single")
    THREE: ClassVar[tuple[int,str]] = (3, "single")
    REPEAT: ClassVar[tuple[int,str]] = (0, "single")
    REPEAT_OPTIONS: ClassVar[tuple[int,str]] = (2, "double")
    EXIT: ClassVar[tuple[int,str]] = (11, "long")

    _allowed_pins: ClassVar[set[int]] = {0, 1, 2, 3, 11}
    _allowed_pins_single: ClassVar[set[int]] = {0, 1, 2, 3}
    _allowed_pins_double: ClassVar[set[int]] = {0,2}
    _allowed_pins_long: ClassVar[set[int]] = {0,11}

    def __init__(self, i2c_bus=None, address=None):
        if i2c_bus is None:
            i2c_bus = busio.I2C(board.SCL, board.SDA)
        if address is None:
            address = self.DEFAULT_MPR121_ADDRESS
        self.mpr121 = adafruit_mpr121.MPR121(i2c_bus, address=address)

    def _help(self):
        """
        Prints the help message for the touch input mixin.
        """
        print(
            "Touch Input Mixin Help:\n"
            "Touch a pin on the MPR121 sensor to trigger an event.\n"
            "Events:\n"
            "  - Single tap: quick touch and release for pins 0-3\n"
            "  - Double tap: two quick touches in succession for pin 0 and 2\n"
            "  - Long press: touch and hold for a longer duration for pins 0 and 11\n"
        )

    def get_input(self):
        """
        Waits for a touch event and returns a tuple:
        (pin_number, event_type) where event_type is 'single', 'double', or 'long'
        """
        while True:
            # note that only the first 4 pins are used in this code
            for pin in self._allowed_pins:
                if self.mpr121[pin].value:
                    start_time = time.time()
                    # Wait until release
                    while self.mpr121[pin].value:
                        time.sleep(0.01)
                    duration = time.time() - start_time

                    # Long press if pin is allowed for long press
                    if (pin in self._allowed_pins_long) and (duration >= self.LONG_PRESS_MIN):
                        return (pin, "long")

                    # check if the pin is allowed for double tap
                    # and if so, check for a second tap coming
                    # and if the second tap is within the DOUBLE_TAP_GAP_MAX
                    # and the duration is within SINGLE_TAP_MAX you got double tap
                    if (pin in self._allowed_pins_double):
                        start_time2 = time.time()
                        while (time.time() - start_time) < self.DOUBLE_TAP_GAP_MAX:
                            if self.mpr121[pin].value:
                                # wait until release
                                while self.mpr121[pin].value:
                                    time.sleep(0.01)
                                duration2 = time.time() - start_time2
                                if duration2 <= self.SINGLE_TAP_MAX:
                                    # If we get here, it was a double tap
                                    return (pin, "double")

                    # final single tap check
                    if (pin in self._allowed_pins_single) and (duration <= self.SINGLE_TAP_MAX):
                        return (pin, "single")
                
            time.sleep(0.01)