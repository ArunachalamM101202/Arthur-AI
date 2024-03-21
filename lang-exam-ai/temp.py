import streamlit as st
from gtts import gTTS
from PIL import Image
import google.generativeai as genai

vision_model = genai.GenerativeModel('gemini-pro-vision')
model = genai.GenerativeModel('gemini-pro')

model_avatar = "model_img.png"

def generate_audio(text):
    tts = gTTS(text, lang='en', tld="us")
    tts.save('output.mp3')

def execute_prompt(prompt):
    response = model.generate_content(prompt)
    return response.text


def execute_prompt_with_image(prompt, image):
    response = vision_model.generate_content([prompt, image], stream=True)
    response.resolve()
    return response.text

def main():
    st.title("Arthur AI")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        
        # Build a list of user messages and model responses for context
        messages = []
        for message in st.session_state.messages:
            role = message["role"]
            parts = message["parts"]
            messages.append({"role": role, "parts": parts})

        # Generate response from Gemini API
        if messages:
            response = model.generate_content(messages)

            # Add model response to chat history
            st.session_state.messages.append({"role": "model", "parts": [response.text]})

            # Display model response in chat
            st.write_stream({"parts": [response.text]})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        role = message["role"]
        parts = message["parts"]
        # with st.chat_message(role):
        #     for part in parts:
        #         st.markdown(part)
        with st.chat_message(role, avatar=None if role == "user" else model_avatar):
            for part in parts:
                if role == "user":
                    st.write(part)  # Display user input directly
                else:
                    st.markdown(part) 


if __name__ == "__main__":
    main()
