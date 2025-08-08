from pathlib import Path
import logging
from playsound3 import playsound

logger = logging.getLogger(__name__)

from ..audio.generic_tts import TextToSpeechConverter

class AudioOutputMixin:
    """
    Mixin class to provide audio output functionality.
    """
    def render_audio(self, text: str, tts_converter: TextToSpeechConverter, output_path: Path) -> Path:
        """
        Render the text as audio with the converter.
        """
        logger.debug(f"Rendering audio to: {output_path.as_posix()}.")
        tts_converter.convert_text_to_speech(
            text=text,
            output_file=output_path.as_posix()
        )
        logger.debug(f"... conversion done.")
        return output_path
    
    def play_audio(self, audio_file: Path) -> None: 
        """
        Play the audio file using the playsound library.
        """
        logger.debug(f"Playing audio file: {audio_file.as_posix()}.")
        playsound(audio_file.as_posix())
        logger.debug("... playback done.")