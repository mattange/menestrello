from dotenv import load_dotenv
load_dotenv()
import logging
from pathlib import Path
from playsound3 import playsound

logger = logging.getLogger(__name__)

from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
logger.debug(f"Root directory: {ROOT_DIR}")
STORIES_DIR = ROOT_DIR / "stories"
logger.debug(f"Stories directory: {STORIES_DIR}")
STORIES_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI()

from menestrello.audio import GoogleTextToSpeechConverter
from menestrello.user import ConsoleUserInteraction, KeyboardUserInteraction

from menestrello.story.story_tree import StoryTree

from menestrello.constants import (
    LLM_MODEL,
    LLM_TEMPERATURE,
)

def main():

    # HERE play audio file with a welcome message
    user_interaction = KeyboardUserInteraction()
    google_tts = GoogleTextToSpeechConverter()
    google_tts.initialize(language_code="it-IT", gender="FEMALE", speaking_rate=1.0)
    response_format = StoryTree.chatbot_response_format()
    
    story = StoryTree(root_location=STORIES_DIR)
    
    user_interaction.provide_output("Welcome to the Interactive Storytelling Chatbot!")
    user_interaction.present_introduction()
    in_story = False
    while True:
        if in_story:
            user_input = user_interaction.get_input()
        else:
            user_input = user_interaction.get_initial_story_prompt()
            in_story = True
        
        if user_input == user_interaction.RESET:
            # Reset the conversation
            story = StoryTree(root_location=STORIES_DIR)
            in_story = False
            continue

        elif user_input == user_interaction.UP:
            story.rewind_up()
            story_fragment = story.current_story_interaction
            if story_fragment is not None:
                # perhaps play audio file 
                user_interaction.provide_output(
                    story_fragment.chatbot.tts_target(
                        include_introduction=True, 
                        include_title=True
                    )
                )
            else:
                story = StoryTree(root_location=STORIES_DIR)
                in_story = False
            continue

        elif user_input == user_interaction.ONE:
            user_input = "1"
        elif user_input == user_interaction.TWO:
            user_input = "2"
        elif user_input == user_interaction.THREE:
            user_input = "3"
        else:
            user_interaction.goodbye()
            break
        
        # Add the user's input to the conversation
        story.chatbot_conversation__append_user_input(user_input)  # type: ignore

        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            response_format=response_format, # type: ignore
            messages=story.chatbot_conversation, # type: ignore
        )
        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        story.chatbot_conversation__append_chatbot_response(assistant_reply)   # type: ignore
        story_fragment = story.current_story_interaction
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