import streamlit as st
import requests
import time
from datetime import datetime
import speech_recognition as sr
# Configuration
API_KEY = st.secrets["API_KEY"] #api key
MODEL = "meta-llama/llama-3-70b-instruct"  # Model name
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_INTERVAL = 10  # Seconds between requests

# Initialize session state
if "conversations" not in st.session_state:
    st.session_state.conversations = [{"id": 1, "messages": [{"role": "assistant", "content": "How can I help you today?"}]}]
if "current_chat" not in st.session_state:
    st.session_state.current_chat = 0
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

# Alias for current messagesss
messages = st.session_state.conversations[st.session_state.current_chat]["messages"]

def get_llama_response(messages):
    # Rate limiting
    elapsed = time.time() - st.session_state.last_request_time
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://llama-assistant.streamlit.app",  # Update with URL
        "X-Title": "LlamaBuddy"
    }

    # Prepare messages with system prompt and conversation history
    api_messages = [
        {"role": "system", "content": "You are LlamaBuddy, an AI assistant powered by LLaMA 3. You can chat naturally, generate code, translate text to English, explain concepts in simple terms, summarize text, rewrite text, brainstorm ideas, and handle various other tasks. Respond appropriately based on the user's request. For code generation, provide executable code. For translations, provide the translated text. For explanations, keep it simple. Always be helpful and accurate."}
    ]
    api_messages.extend(messages)  # Add the conversation history

    payload = {
        "model": MODEL,
        "messages": api_messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=45  # Increased timeout
        )

        response.raise_for_status()
        st.session_state.last_request_time = time.time()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.text}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
    return None

def generate_images(pipe, prompt, params):
    try:
        images = pipe(prompt, **params).images
        return images
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return []

# Streamlit UI
st.set_page_config(page_title="Olivia - AI Assistant")
st.title("Olivia")


# Theme selection
if "theme" not in st.session_state:
    st.session_state.theme = "light"
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
if theme != st.session_state.theme:
    st.session_state.theme = theme
    st.rerun()

if st.session_state.theme == "Dark":
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .stChatMessage {
            background-color: #1f2937;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #1f2937;
            color: white;
            border-color: #374151;
        }
        .stButton > button {
            background-color: #374151;
            color: white;
        }
        .stSidebar {
            background-color: #111827;
            color: white;
        }
        .stRadio > div {
            color: white;
        }
        .stSelectbox > div {
            background-color: #1f2937;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# The AI can handle various tasks automatically based on your prompt.
# For example: "Translate this text", "Explain quantum physics", "Write Python code for a calculator"

st.sidebar.header("Chats")
for i, conv in enumerate(st.session_state.conversations):
    if st.sidebar.button(f"Chat {conv['id']}", key=f"chat_{i}"):
        st.session_state.current_chat = i
        st.rerun()

if st.sidebar.button("New Chat"):
    new_id = len(st.session_state.conversations) + 1
    st.session_state.conversations.append({"id": new_id, "messages": [{"role": "assistant", "content": "How can I help you today?"}]})
    st.session_state.current_chat = len(st.session_state.conversations) - 1
    st.rerun()

# Clear current chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.conversations[st.session_state.current_chat]["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]
    st.rerun()

# Display chat history
for i, message in enumerate(messages):
    with st.chat_message(message["role"]):
        if "```" in message["content"]:
            st.code(message["content"], language="python")
        else:
            st.write(message["content"])
    if message["role"] == "assistant":
        if st.button("Say Something", key=f"voice_reply_{i}"):
            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                st.info("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                text = recognizer.recognize_google(audio)
                st.success(f"Transcribed: {text}")
                prompt = text
                messages.append({"role": "user", "content": prompt})
                with st.spinner("Generating response..."):
                    response = get_llama_response(messages)
                if response:
                    messages.append({"role": "assistant", "content": response})
                else:
                    st.warning("Failed to get response. Please check your API key and try again.")
            except sr.UnknownValueError:
                st.error("Could not understand the audio")
            except sr.RequestError as e:
                st.error(f"Speech recognition error: {e}")



# User input
if prompt := st.chat_input("Type your message..."):
    messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = get_llama_response(messages)
        
        if response:
            if "```" in response:
                st.code(response, language="python")
            else:
                st.write(response)
            messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Failed to get response. Please check your API key and try again.")
