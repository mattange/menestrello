import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

from menestrello.llm_chat_setup import llm_chat_setup
from menestrello.text_to_speech import text_to_speech

def main():

    conversation = llm_chat_setup()
    print("Welcome to the Interactive Storytelling Chatbot!")
    print("Type 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add the user's input to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Get the chatbot's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract the assistant's reply
        assistant_reply = response["choices"][0]["message"]["content"]
        print(f"Chatbot: {assistant_reply}")

        # Convert the assistant's reply to speech
        output_path = "assistant_reply.mp3"
        text_to_speech(assistant_reply, output_path)
        print(f"Audio content written to file: {output_path}")

        # Play the audio file (this part is platform-dependent and may require additional libraries)      

        # Add the assistant's reply to the conversation
        conversation.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()