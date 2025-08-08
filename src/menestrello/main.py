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
from menestrello.user import ConsoleUserIO, KeyboardUserIO

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

    # HERE play audio file with a welcome message
    user_interaction = KeyboardUserIO()
    google_tts = GoogleTextToSpeechConverter()
    google_tts.initialize(
        language_code=GOOGLE_TTS_LANG, 
        gender=GOOGLE_TTS_GENDER, 
        speaking_rate=GOOGLE_TTS_RATE,
        pitch=GOOGLE_TTS_PITCH,
    )
    response_format = StoryTree.chatbot_response_format()
    
    user_interaction.story = StoryTree(root_location=STORIES_DIR)
    user_interaction.present_introduction()

    while True:
        if len(user_interaction.story) > 0:
            user_input = user_interaction.get_input()
        else:
            user_input = user_interaction.get_initial_story_prompt()
        
        if user_input == user_interaction.RESET:
            # Reset the conversation
            user_interaction.story = StoryTree(root_location=STORIES_DIR)
            continue

        elif user_input == user_interaction.UP:
            user_interaction.story.rewind_up()
            story_fragment = user_interaction.story.current_story_interaction
            if story_fragment is not None:
                # perhaps play audio file 
                user_interaction.provide_output(
                    story_fragment.chatbot.tts_target(
                        include_introduction=True, 
                        include_title=True
                    )
                )
            else:
                user_interaction.story = StoryTree(root_location=STORIES_DIR)
            continue

        # handle user input if you want to repeat the options
        elif user_input == user_interaction.REPEAT:
            if user_interaction.story.current_story_interaction is not None:
                user_interaction.provide_output(
                    user_interaction.story.current_story_interaction.chatbot.tts_target(
                        include_introduction=False, 
                        include_title=False,
                        include_frgment=False,
                        include_question=True,
                        include_options=True,
                    )
                )
            continue

        elif user_input == user_interaction.ONE:
            user_input = "1"
        elif user_input == user_interaction.TWO:
            user_input = "2"
        elif user_input == user_interaction.THREE:
            user_input = "3"
        else:
            # exit basically doing same as reset
            user_interaction.goodbye()
            user_interaction.story = StoryTree(root_location=STORIES_DIR)
            continue

        # Add the user's input to the conversation
        user_interaction.story.chatbot_conversation__append_user_input(user_input)  # type: ignore

        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            response_format=response_format, # type: ignore
            messages=story.chatbot_conversation, # type: ignore
        )
        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        user_interaction.story.chatbot_conversation__append_chatbot_response(assistant_reply)   # type: ignore
        story_fragment = user_interaction.story.current_story_interaction
        if story_fragment is None:
            user_interaction.provide_output("No story fragment available.")
            continue
        
        # Play the audio file
        # audio_file = story_fragment.render_audio(tts_converter=google_tts)
        # logger.debug(f"Playing audio file: {audio_file.as_posix()}")
        # sound = playsound(audio_file.as_posix())

        user_interaction.provide_output(
            story_fragment.chatbot.tts_target(
                include_introduction=True, 
                include_title=True
            )
        )

if __name__ == "__main__":
    main()