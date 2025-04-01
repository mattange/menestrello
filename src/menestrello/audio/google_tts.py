import logging
from google.cloud import texttospeech

logger = logging.getLogger(__name__)

def google_tts(text, output_path, language_code="en-GB", gender="NEUTRAL", speaking_rate=1.0, pitch=0.0):
    """
    Converts text to speech using Google Cloud Text-to-Speech API and saves the audio to a file.

    Args:
        text (str): The text to be converted to speech.
        output_path (str): The file path where the audio file will be saved.
        language_code (str): The language code for the voice (e.g., "en-US").
        gender (str): The gender of the voice ("MALE", "FEMALE", "NEUTRAL").
        speaking_rate (float): The speaking rate of the voice (default is 1.0).
        pitch (float): The pitch of the voice (default is 0.0).

    Returns:
        None
    """
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    gender_enum = getattr(texttospeech.SsmlVoiceGender, gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=gender_enum,
        name=f"{language_code}-Chirp3-HD-Aoede"
    )

    # Configure the audio settings
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=0.0,
        # sample_rate_hertz=24000,
        # below seems not to work despite documentation
        # effects_profile_id=["small-bluetooth-speaker-class-device"],
    )

    logger.debug("Calling API to perform conversion of text to speech")
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Write the response to the output file
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        logger.info(f"Audio content written to file: {output_path}")