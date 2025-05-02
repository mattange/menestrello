from dotenv import load_dotenv
load_dotenv()
import logging
from treelib import Tree
from pathlib import Path

logger = logging.getLogger(__name__)

from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
logger.debug(f"Root directory: {ROOT_DIR}")
STORIES_DIR = ROOT_DIR / "stories"
logger.debug(f"Data directory: {STORIES_DIR}")
STORIES_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI()

from menestrello.llm import chat_setup, InteractionResponseFormat
from menestrello.audio import GoogleTextToSpeechConverter
from menestrello.user import ConsoleUserInteraction

from menestrello.constants import (
    LLM_MODEL,
    LLM_TEMPERATURE,
)

def main():

    # HERE play audio file with a welcome message
    print("Welcome to the Interactive Storytelling Chatbot!\n")
    print("Type 'exit' to end the conversation.")
    print("You can also type 'reset' to reset the conversation.")

    user_interaction = ConsoleUserInteraction()
    google_tts = GoogleTextToSpeechConverter()
    google_tts.initialize(language_code="it-IT", gender="FEMALE", speaking_rate=1.0)

    stories_tree = Tree()
    stories_tree.create_node("Stories", "stories")  # Root node
    current_story_node = stories_tree.create_node("story_1", 1, parent="stories")
    current_story_tree = stories_tree.subtree(1)
    STORY_DIR = STORIES_DIR / current_story_node.tag
    STORY_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Story directory: {STORY_DIR}")
    conversation = chat_setup()
    current_story_step = 0
    
    while True:
        user_input = user_interaction.get_input()

        if user_input == user_interaction.EXIT_COMMAND:
            print("Goodbye!")
            break
        
        if user_input == user_interaction.RESET_COMMAND:
            # Reset the conversation
            print("Story reset.")
            conversation = chat_setup()
            new_story_node = stories_tree.create_node(f"story_{current_story_node.identifier + 1}", current_story_node.identifier + 1, parent="stories")
            current_story_node = new_story_node
            current_story_tree = stories_tree.subtree(current_story_node.identifier)
            STORY_DIR = STORIES_DIR / current_story_node.tag
            STORY_DIR.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Story directory: {STORY_DIR}")
            continue
        
        # Add the user's input to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Get the chatbot's response
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=conversation,
            temperature=LLM_TEMPERATURE,
            # TODO Add temperature and other parameters to the request
            # TODO Add response format that is not text and is a pydantic model
            # response_format="text",
        )

        # # Extract the assistant's reply        
        assistant_reply = response.choices[0].message.content
        print(f"Chatbot: {assistant_reply}")
        
        new_story_node = current_story_tree.create_node(
            f"Fragment: {current_story_step + 1}",
            (current_story_node.identifier, current_story_step + 1),
            parent=current_story_node.identifier,
        )
        current_story_node = new_story_node
        current_story_step += 1

        # Add the assistant's reply to the conversation
        conversation.append({"role": "assistant", "content": assistant_reply})

        # Convert the assistant's reply to speech
        output_path = STORY_DIR / f"fragment_{current_story_step}.mp3"
        google_tts.convert_text_to_speech(assistant_reply, output_path)
        print(f"Audio content written to file: {output_path}")

        # Play the audio file (this part is platform-dependent and may require additional libraries)      


if __name__ == "__main__":
    main()