from dotenv import load_dotenv
load_dotenv()
import logging
from pathlib import Path
import os
import argparse
import importlib

logger = logging.getLogger(__name__)

from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
logger.debug(f"Root directory: {ROOT_DIR}")
STORIES_DIR = Path(os.getenv("MENESTRELLO_STORIES_DIR", ROOT_DIR / "stories"))
logger.debug(f"Stories directory: {STORIES_DIR}")
STORIES_DIR.mkdir(parents=True, exist_ok=True)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
logger.debug(f"Environment: {ENVIRONMENT}")

client = OpenAI()

from menestrello.audio import GoogleTextToSpeechConverter

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

    parser = argparse.ArgumentParser(description="Menestrello main entry point")
    parser.add_argument("--io-class", 
                        type=str, 
                        required=False,
                        default=os.getenv("MENESTRELLO_IO_CLASS","ConsoleUserIO"), 
                        help=(
                            "User IO class name from menestrello.user. "
                            "Defaults to environment variable MENESTRELLO_IO_CLASS or 'ConsoleUserIO'."
                        ),
                        )
    args = parser.parse_args()

    # Dynamically import the class from menestrello.user
    user_module = importlib.import_module("menestrello.user")
    try:
        UserIO = getattr(user_module, args.io_class)
        user_interaction = UserIO()
    except AttributeError:
        logger.error(f"User IO class '{args.io_class}' not found in menestrello.user")
        raise RuntimeError(f"User IO class '{args.io_class}' not found in menestrello.user")

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
            user_interaction.provide_output(
                None,
                play_initial_holding_audio=True,
                play_holding_audio=False
            )
            user_input = user_interaction.get_initial_story_prompt()
            # you don't need to check if the user input is empty
            # as the get_initial_story_prompt() will always return a string
            # then ask the chatbot for the first story fragment

        # handle user input to rewind up a level in the story
        elif user_input == user_interaction.UP:
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
            # continue to the next iteration
            continue

        # handle user input if you want to repeat the options only
        elif user_input == user_interaction.REPEAT_OPTIONS:
            story_fragment = user_interaction.story.current_story_interaction
            if (story_fragment is not None) and (story_fragment.chatbot.options): # type: ignore
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

        # handle user input if you want to repeat the whole story fragment
        elif user_input == user_interaction.REPEAT:
            story_fragment = user_interaction.story.current_story_interaction
            if story_fragment is not None:
                # this is the same as at bottom of the loop
                # but as it should be there already, we don't need
                # the holding audio
                user_interaction.provide_output(
                    story_fragment.chatbot.tts_target( # type: ignore
                        include_introduction=True, 
                        include_title=True
                    ),
                    tts_converter=google_tts,
                    output_path=story_fragment.storage_folder / "fragment.mp3", # type: ignore
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
        
        include_title = (len(user_interaction.story) == 1)
        user_interaction.provide_output(
            story_fragment.chatbot.tts_target( # type: ignore
                include_introduction=True, 
                include_title=include_title
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