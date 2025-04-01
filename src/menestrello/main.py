from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

# Set your OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

from menestrello.llm import chat_setup
from menestrello.audio import google_tts

def main():

    model, conversation = chat_setup()
    print("Welcome to the Interactive Storytelling Chatbot!")
    print("Type 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # # Add the user's input to the conversation
        # conversation.append({"role": "user", "content": user_input})

        # # Get the chatbot's response
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=conversation
        # )

        # # Extract the assistant's reply
        # assistant_reply = response["choices"][0]["message"]["content"]
        # print(f"Chatbot: {assistant_reply}")

        assistant_reply = (
            "This is the story of a unicorn who lived in a magical forest."
            "One day, the unicorn met a dragon who was lost and needed help."
            "The unicorn used its magic to guide the dragon back home."
            "Along the way, they encountered various challenges, but together they overcame them."
            "In the end, the unicorn and the dragon became the best of friends."
            "They learned that friendship knows no bounds and that helping others is the greatest adventure of all."
        )

        # Convert the assistant's reply to speech
        output_path = "assistant_reply_2.mp3"
        google_tts(assistant_reply, output_path)
        print(f"Audio content written to file: {output_path}")

        # Play the audio file (this part is platform-dependent and may require additional libraries)      

        # Add the assistant's reply to the conversation
        conversation.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()