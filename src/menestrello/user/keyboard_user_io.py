from .generic_user_io import GenericUserIO
from .text_output_mixin import TextOutputMixin
from .audio_output_mixin import AudioOutputMixin
from .keyboard_input_mixin import KeyboardInputMixin
from .random_story_prompt_mixin import RandomStoryPromptMixin

class KeyboardUserIO(KeyboardInputMixin, TextOutputMixin, GenericUserIO):
    pass

class AudioOutputKeyboardInputUserIO(KeyboardInputMixin, AudioOutputMixin, GenericUserIO):
    """
    Class to handle user input and output with audio output capabilities.
    Combines keyboard input and text output with audio output functionality.
    """
    pass

class RandomStoryAudioOutputKeyboardInputUserIO(RandomStoryPromptMixin, AudioOutputKeyboardInputUserIO):
    pass