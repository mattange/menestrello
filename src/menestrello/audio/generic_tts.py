from abc import ABC, abstractmethod

class TextToSpeechConverter(ABC):

    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """
        Initializes the text-to-speech converter. 
        This method should be called before using the converter.
        """
        pass
    
    @abstractmethod
    def convert_text_to_speech(self, text: str, output_file: str) -> None:
        """
        Converts the given text to speech and saves it to the specified output file.

        Args:
            text (str): The text to be converted to speech.
            output_file (str): The path where the audio file will be saved.
        """
        pass
