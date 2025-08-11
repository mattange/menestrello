from .generic_user_io import GenericUserIO
from .text_output_mixin import TextOutputMixin
from .audio_output_mixin import AudioOutputMixin
from .random_story_prompt_mixin import RandomStoryPromptMixin
from .touch_input_mixin import TouchInputMixin

class RandomStoryTouchInputUserIO(
    RandomStoryPromptMixin, 
    TouchInputMixin, 
    TextOutputMixin, 
    GenericUserIO
):
    pass

class RandomStoryTouchInputAudioOutputUserIO(
    RandomStoryPromptMixin,
    TouchInputMixin, 
    AudioOutputMixin, 
    GenericUserIO
):
    pass
