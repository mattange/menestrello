import pytest
import platform

skip_reason = "This test requires a physical MPR121 sensor connected to the I2C bus and ARM64 architecture."
skip_reason = "This test requires Linux OS and aarch64 architecture."
skip_if_not_linux_aarch64 = not (
    platform.system() == "Linux" and platform.machine() == "aarch64"
)


@pytest.mark.skipif(skip_if_not_linux_aarch64, reason=skip_reason)
def test_touch_input_mixin(monkeypatch):
    """
    Manual test for TouchInputMixin. 
    Prints the pin and event type when a touch is detected.
    """
    # This test is intended for manual verification.
    # It will run until a touch is detected.
    from menestrello.user.touch_input_mixin import TouchInputMixin
    
    mixin = TouchInputMixin()
    print("Touch a pin on the MPR121 sensor (single tap, double tap, or long press)...")
    result = mixin.get_input()
    assert isinstance(result, tuple), "Result should be a tuple (pin, event_type)"
    pin, event_type = result
    assert 0 <= pin < 12, "Pin should be between 0 and 11"
    assert event_type in ("single", "double", "long"), "Event type should be 'single', 'double', or 'long'"
    print(f"Detected: pin={pin}, event_type={event_type}")