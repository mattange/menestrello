from dotenv import load_dotenv
load_dotenv()

from menestrello.audio import GoogleTextToSpeechConverter
from .constants import GOOGLE_TTS_GENDER, GOOGLE_TTS_LANG, GOOGLE_TTS_RATE, GOOGLE_TTS_PITCH
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="Generate static audio using Google TTS.")
    parser.add_argument("--text", type=str, required=True, help="Text to convert to speech.")
    parser.add_argument("--output_file", type=str, required=True, help="Output MP3 file path.")
    args = parser.parse_args()
    text = args.text
    output_file = args.output_file

    google_tts = GoogleTextToSpeechConverter()
    google_tts.initialize(
        language_code=GOOGLE_TTS_LANG, 
        gender=GOOGLE_TTS_GENDER, 
        speaking_rate=GOOGLE_TTS_RATE,
        pitch=GOOGLE_TTS_PITCH,
    )
    google_tts.convert_text_to_speech(
        text=text,
        output_file=output_file,
    )

if __name__ == "__main__":
    main()