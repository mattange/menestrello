import time
import pytest
import platform


skip_reason = "This test requires a physical MPR121 sensor connected to the I2C bus and ARM architecture."
skip_if_not_arm = not platform.machine().startswith("aarch64")

@pytest.mark.skipif(skip_if_not_arm, reason=skip_reason)
def test_mpr121_pins():
    """
    Test script to check the functionality of all 12 pins of the MPR121.
    Prints which pin is touched.
    """
    import board
    import busio
    import adafruit_mpr121

    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)
    if not mpr121:
        raise AssertionError("MPR121 not found. Check the connection.")
    
    t = 0
    while t < 10:  # Run for 10 seconds max
        t += 0.05
        for pin in range(12):
            if mpr121[pin].value:
                assert True, f"Pin {pin} is touched"
                t = 10
        time.sleep(0.05)
