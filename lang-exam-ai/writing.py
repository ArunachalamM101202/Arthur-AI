import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai
import os
from streamlit_lottie import st_lottie
import requests
import json

# Function to load and display Lottie animation
@st.cache_data()
def lottie_local(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key is not set. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Set up the Gemini model for fine-tuning
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

model_avatar = "model_img.png"

toefl_writing_str = ""
with open("lang-exam-ai/custom_prompt/toefl_writing_user.txt", "r") as toefl_writing_user:
    toefl_writing_str = toefl_writing_user.read()

toefl_writing_str_model = ""
with open("lang-exam-ai/custom_prompt/toefl_writing_model.txt", "r") as toefl_writing_user:
    toefl_writing_str_model = toefl_writing_user.read()

toefl_reading_str = ""
with open("lang-exam-ai/custom_prompt/toefl_reading_user.txt","r") as toefl_reading_user:
    toefl_reading_str=toefl_reading_user.read()

toefl_reading_str_model = ""
with open("lang-exam-ai/custom_prompt/toefl_reading_model.txt","r") as toefl_reading_user:
    toefl_reading_str_model=toefl_reading_user.read()

gre_verbal_str = ""
with open("lang-exam-ai/custom_prompt/gre_verbal_user.txt","r") as toefl_reading_user:
    gre_verbal_str=toefl_reading_user.read()

gre_verbal_str_model = ""
with open("lang-exam-ai/custom_prompt/gre_verbal_model.txt","r") as toefl_reading_user:
    gre_verbal_str_model=toefl_reading_user.read()

ielts_reading_str = ""
with open("lang-exam-ai/custom_prompt/ielts_reading_user.txt","r") as toefl_reading_user:
    ielts_reading_str=toefl_reading_user.read()

ielts_reading_str_model = ""
with open("lang-exam-ai/custom_prompt/ielts_reading_model.txt","r") as toefl_reading_user:
    ielts_reading_str_model=toefl_reading_user.read()

ielts_writing_str = ""
with open("lang-exam-ai/custom_prompt/ielts_writing_user.txt","r") as toefl_reading_user:
    ielts_writing_str=toefl_reading_user.read()

ielts_writing_str_model = ""
with open("lang-exam-ai/custom_prompt/ielts_writing_model.txt","r") as toefl_reading_user:
    ielts_writing_str_model=toefl_reading_user.read()

german_reading_str = ""
with open("lang-exam-ai/custom_prompt/german_reading_user.txt","r") as toefl_reading_user:
    german_reading_str=toefl_reading_user.read()

german_reading_str_model = ""
with open("lang-exam-ai/custom_prompt/german_reading_model.txt","r") as toefl_reading_user:
    german_reading_str_model=toefl_reading_user.read()

german_writing_str = ""
with open("lang-exam-ai/custom_prompt/german_writing_user.txt","r") as toefl_reading_user:
    german_writing_str=toefl_reading_user.read()

german_writing_str_model = ""
with open("lang-exam-ai/custom_prompt/german_writing_model.txt","r") as toefl_reading_user:
    german_writing_str_model=toefl_reading_user.read()

french_reading_str = ""
with open("lang-exam-ai/custom_prompt/french_reading_user.txt","r") as toefl_reading_user:
    french_reading_str=toefl_reading_user.read()

french_reading_str_model = ""
with open("lang-exam-ai/custom_prompt/french_reading_model.txt","r") as toefl_reading_user:
    french_reading_str_model=toefl_reading_user.read()

def main():
    # Sidebar for selecting exam type
    # st.sidebar.image("https://media.giphy.com/media/S60CrN9iMxFlyp7uM8/giphy.gif?cid=790b7611l1yct98bgj4lm0205cu71rf1hyrbgi081lx92ga1&ep=v1_gifs_search&rid=giphy.gif&ct=g",width=200)

    with st.sidebar:
        anim = lottie_local('lang-exam-ai/chatbot_animation.json')
        st_lottie(anim,
                speed=1,
                reverse=False,
                loop=True,
                height = 130,
                width = 250,
                quality="high",
            key=None)

    st.sidebar.markdown("""
### Arthur AI - Language Exam Practice Assistant

Arthur AI is your personalized language exam practice assistant developed by Team AllStars and powered by state-of-the-art natural language processing models. Whether you're preparing for exams like TOEFL, GRE, IELTS, or language proficiency tests like German (A1) and French (A1). Arthur AI is here to help you improve your skills.
""")
    
    exam_type = st.sidebar.selectbox("Select Exam Type you wish to practice", ("TOEFL Reading", "TOEFL Writing", "GRE Verbal", "IELTS Reading","IELTS Writing","German - A1 Reading (Lesen)","German - A1 Writing (Schreiben)","French - A1 Reading (lecture)"))

    st.title(f"Arthur AI - {exam_type}")
    
    # Initialize chat history for each exam type
    if exam_type not in st.session_state:
        st.session_state[exam_type] = []

    # React to user input for selected exam type
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.session_state[exam_type].append({"role": "user", "parts": [prompt]})
        
        # Build a list of user messages and model responses for context
        messages = []
        for message in st.session_state[exam_type]:
            role = message["role"]
            parts = message["parts"]
            messages.append({"role": role, "parts": parts})

        # If Writing is selected, interact with the fine-tuned Gemini model
        if exam_type == "TOEFL Writing":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [toefl_writing_str]
                },
                {
                    "role": "model",
                    "parts": [toefl_writing_str_model]
                },
            ])
            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "TOEFL Reading":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [toefl_reading_str]
                },
                {
                    "role": "model",
                    "parts": [toefl_reading_str_model]
                },
            ])
            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "GRE Verbal":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [gre_verbal_str]
                },
                {
                    "role": "model",
                    "parts": [gre_verbal_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "IELTS Reading":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [ielts_reading_str]
                },
                {
                    "role": "model",
                    "parts": [ielts_reading_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "IELTS Writing":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [ielts_writing_str]
                },
                {
                    "role": "model",
                    "parts": [ielts_writing_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "German - A1 Reading (Lesen)":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [german_reading_str]
                },
                {
                    "role": "model",
                    "parts": [german_reading_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "German - A1 Writing (Schreiben)":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [german_writing_str]
                },
                {
                    "role": "model",
                    "parts": [german_writing_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        elif exam_type == "French - A1 Reading (lecture)":
            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [french_reading_str]
                },
                {
                    "role": "model",
                    "parts": [french_reading_str_model]
                },
            ])

            convo.send_message(prompt)
            response = convo.last.text
        else:
            
            response = model.generate_content(messages).text

        # Add model response to chat history
        st.session_state[exam_type].append({"role": "model", "parts": [response]})

        # to remove \n
        response_with_br = response.replace('\n', '<br>')
        st.write_stream({"parts": [response_with_br]})

    # Display chat messages from history on app rerun for selected exam type
    for message in st.session_state[exam_type]:
        role = message["role"]
        parts = message["parts"]
        with st.chat_message(role, avatar=None if role == "user" else model_avatar):
            for part in parts:
                if role == "user":
                    st.write(part)  # Display user input directly
                else:
                    st.markdown(part) 

if __name__ == "__main__":
    main()
