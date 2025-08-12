import platform

if ( 
    platform.system() == "Windows" 
    ) or (
        (platform.system() == "Linux") and (platform.machine() != "aarch64")
    ):
    try:
        from .keyboard_user_io import (
            KeyboardUserIO,
            AudioOutputKeyboardInputUserIO,
            RandomStoryAudioOutputKeyboardInputUserIO,
        )
    except ImportError as e:
        pass

if (platform.system() == "Linux") and (platform.machine() == "aarch64"):
    # import touch user IO for Linux
    # as you need the sensor and it's on raspberry pi
    from .touch_user_io import RandomStoryTouchInputAudioOutputUserIO

from .console_user_io import ConsoleUserIO
