from playsound3 import playsound
from pathlib import Path

def test_sound_player():
    test_folder = Path(__file__).parent
    test_audio_file = test_folder / "file_for_test.mp3"
    try:
        _ = playsound(test_audio_file.as_posix())
        assert True, "Sound played successfully"
    except Exception as e:
        raise AssertionError(f"Failed to play sound: {e}")