from dotenv import load_dotenv
load_dotenv()
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
logger.debug(f"Root directory: {ROOT_DIR}")
STORIES_DIR = ROOT_DIR / "stories"
logger.debug(f"Stories directory: {STORIES_DIR}")
STORIES_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI()

from menestrello.audio import GoogleTextToSpeechConverter
from menestrello.user import (
    ConsoleUserIO, 
    KeyboardUserIO, 
    AudioOutputKeyboardInputUserIO,
    RandomStoryAudioOutputKeyboardInputUserIO,
)

from menestrello.story.story_tree import StoryTree

from menestrello.constants import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    GOOGLE_TTS_LANG,
    GOOGLE_TTS_GENDER,
    GOOGLE_TTS_RATE,
    GOOGLE_TTS_PITCH,
)

def main():

    user_interaction = KeyboardUserIO()
    # user_interaction = ConsoleUserIO()
    # user_interaction = AudioOutputKeyboardInputUserIO()
    # user_interaction = RandomStoryAudioOutputKeyboardInputUserIO()

    google_tts = GoogleTextToSpeechConverter()
    google_tts.initialize(
        language_code=GOOGLE_TTS_LANG, 
        gender=GOOGLE_TTS_GENDER, 
        speaking_rate=GOOGLE_TTS_RATE,
        pitch=GOOGLE_TTS_PITCH,
    )
    response_format = StoryTree.chatbot_response_format()
    
    user_interaction.present_introduction()

    while True:

        user_input = user_interaction.get_input()

        if (user_interaction.story is not None) and (len(user_interaction.story) > 0):
            play_holding_audio = True
        else:
            play_holding_audio = False

        # handle user input to start the conversation
        # at any point in the story or at the beginning
        if (user_input == user_interaction.START) or (user_interaction.story is None):
            # Reset the conversation
            user_interaction.story = StoryTree(root_location=STORIES_DIR)
            user_input = user_interaction.get_initial_story_prompt()

        # handle user input to rewind up a level in the story
        if user_input == user_interaction.UP:
            user_interaction.story.rewind_up()
            story_fragment = user_interaction.story.current_story_interaction
            if story_fragment is not None:
                user_interaction.provide_output(
                    story_fragment.chatbot.tts_target(
                        include_introduction=False, 
                        include_title=True
                    ),
                    tts_converter=google_tts,
                    output_path=story_fragment.storage_folder / "fragment_wo_introduction.mp3",
                    play_holding_audio=False,
                )
            else:
                user_interaction.story = StoryTree(root_location=STORIES_DIR)
                user_interaction.present_introduction()
            continue

        # handle user input if you want to repeat the options
        elif user_input == user_interaction.REPEAT:
            story_fragment = user_interaction.story.current_story_interaction
            if story_fragment is not None:
                user_interaction.provide_output(
                    story_fragment.chatbot.tts_target(
                        include_introduction=False, 
                        include_title=False,
                        include_fragment=False,
                        include_question=True,
                        include_options=True,
                    ),
                    tts_converter=google_tts,
                    output_path=story_fragment.storage_folder / "fragment_options.mp3",
                    play_holding_audio=False,
                )
            continue
        
        # handle user input for the options
        elif user_input == user_interaction.ONE:
            user_input = "1"
        elif user_input == user_interaction.TWO:
            user_input = "2"
        elif user_input == user_interaction.THREE:
            user_input = "3"

        # handle user input to exit the application
        elif user_input == user_interaction.EXIT:
            user_interaction.goodbye()
            break

        
        # here we are at a situation where a problem may arise:
        # we have rewound up in the story, and the user may choose an option
        # that we created already or not. if not, the code below works fine as 
        # it will create a new one in the conversation
        # also the chatbot conversation that you see in the story tree is misleading
        # as it may not reflect the actual conversation
        # so you have to:
        # 1. check if the current step has children in the story tree with the same option
        # 2. if so, return the story_fragment as that one to be rerendered
        # 3. if not proceed with the below 

        # check if the user input matches any of the options under the current step
        assert(isinstance(user_input,str))
        story_fragment = user_interaction.story.check_user_input_under_current_step(user_input)

        if story_fragment is  None:
            # Add the user's input to the conversation
            user_interaction.story.chatbot_conversation__append_user_input(user_input)  # type: ignore

            response = client.chat.completions.create(
                model=LLM_MODEL,
                temperature=LLM_TEMPERATURE,
                response_format=response_format, # type: ignore
                messages=user_interaction.story.chatbot_conversation, # type: ignore
            )
            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content

            user_interaction.story.chatbot_conversation__append_chatbot_response(assistant_reply)   # type: ignore
            story_fragment = user_interaction.story.current_story_interaction

        # if story_fragment is None:
        #     user_interaction.provide_output(
        #         "No story fragment available.",
        #         tts_converter=google_tts,
        #         output_path="./no_story_error.mp3",
        #     )
        #     continue
        
        user_interaction.provide_output(
            story_fragment.chatbot.tts_target( # type: ignore
                include_introduction=True, 
                include_title=True
            ),
            tts_converter=google_tts,
            output_path=story_fragment.storage_folder / "fragment.mp3", # type: ignore
            play_holding_audio=play_holding_audio,
        )

        # now check if the story fragment has options
        # and if not, then loop back to the beginning
        if not story_fragment.chatbot.options: # type: ignore
            user_interaction.story = None

if __name__ == "__main__":
    main()