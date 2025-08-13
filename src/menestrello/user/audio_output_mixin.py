from pathlib import Path
import logging
from playsound3 import playsound
from pathlib import Path
import random

logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve().parent
statics_dir = current_dir / "audio_output_mixin_static"

from ..audio.generic_tts import TextToSpeechConverter

class AudioOutputMixin:
    """
    Mixin class to provide audio output functionality.
    """
    def _render_audio(self, text: str, tts_converter: TextToSpeechConverter, output_path: Path) -> Path:
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
    
    def _play_audio(self, audio_file: Path) -> None: 
        """
        Play the audio file using the playsound library.
        """
        logger.debug(f"Playing audio file: {audio_file.as_posix()}.")
        playsound(audio_file.as_posix())
        logger.debug("... playback done.")
    
    def provide_output(self, message: str | None = None, **kwargs) -> None:
        """
        Provide output to the user.
        """
        if message:
            tts_converter = kwargs.get("tts_converter", None)
            output_path = kwargs.get("output_path", None)
            play_holding_audio = kwargs.get("play_holding_audio", False)
            play_initial_holding_audio = kwargs.get("play_initial_holding_audio", False)
            assert tts_converter is not None and output_path is not None, "TTS converter and output_path must be provided."
            if not output_path.exists():
                if play_holding_audio or play_initial_holding_audio:
                    logger.debug("Need to create new audio, playing holding audio.")
                    if play_initial_holding_audio:
                        holding_audio_path = statics_dir / "holding_initial.mp3"
                    else:
                        holding_audio_path = statics_dir / random.choice([
                            "holding_1.mp3", 
                            "holding_2.mp3", 
                            "holding_3.mp3",
                            "holding_4.mp3",
                        ])
                    if holding_audio_path.exists():
                        self._play_audio(holding_audio_path)
                    else:
                        logger.warning(f"Holding audio file not found: {holding_audio_path.as_posix()}")
                self._render_audio(message, tts_converter, output_path)
            self._play_audio(output_path)
        else:
            logger.warning("No message provided for audio output.")

    def present_introduction(self) -> None:
        """
        Present the introduction to the user.
        """
        intro_audio_path = statics_dir / "introduction.mp3"
        if intro_audio_path.exists():
            self._play_audio(intro_audio_path)
        else:
            logger.warning(f"Introduction audio file not found: {intro_audio_path.as_posix()}")
        
    def goodbye(self) -> None:
        """
        Provide a goodbye message to the user.
        """
        goodbye_audio_path = statics_dir / "goodbye.mp3"
        if goodbye_audio_path.exists():
            self._play_audio(goodbye_audio_path)
        else:
            logger.warning(f"Goodbye audio file not found: {goodbye_audio_path.as_posix()}")
