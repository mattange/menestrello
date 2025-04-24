import logging
from google.cloud import texttospeech

logger = logging.getLogger(__name__)

from .generic_tts import TextToSpeechConverter

class GoogleTextToSpeechConverter(TextToSpeechConverter):

    def initialize(self, *args, **kwargs) -> None:
        self.client = texttospeech.TextToSpeechClient()
        
        self.language_code = kwargs.get("language_code", "en-GB")
        self.gender = kwargs.get("gender", "NEUTRAL")
        self.speaking_rate = kwargs.get("speaking_rate", 1.0)
        self.pitch = kwargs.get("pitch", 0.0)
        self.effects_profile_id = kwargs.get("effects_profile_id", ["small-bluetooth-speaker-class-device"])
        self.audio_encoding = kwargs.get("audio_encoding", texttospeech.AudioEncoding.MP3)
        self.sample_rate_hertz = kwargs.get("sample_rate_hertz", 48000)
        self.volume_gain_db = kwargs.get("volume_gain_db", 0.0)

        # Configure the voice request
        gender_enum = getattr(texttospeech.SsmlVoiceGender, self.gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            ssml_gender=gender_enum,
            name=f"{self.language_code}-Chirp3-HD-Aoede",
        )

        # Configure the audio settings
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
            volume_gain_db=self.volume_gain_db,
            sample_rate_hertz=self.sample_rate_hertz,
            # below seems not to work despite documentation
            effects_profile_id=self.effects_profile_id,
        )

    def convert_text_to_speech(self, text: str, output_file: str) -> None:
        """
        Converts the given text to speech and saves it to the specified output file.

        Args:
            text (str): The text to be converted to speech.
            output_file (str): The path where the audio file will be saved.
        """
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        logger.debug("Calling API to perform conversion of text to speech")
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        logger.debug("Writing audio content to file: {output_file}")
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            logger.debug(f"... done")