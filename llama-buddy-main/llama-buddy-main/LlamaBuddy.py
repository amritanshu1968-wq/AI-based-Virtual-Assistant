import streamlit as st
import requests
import time
from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import io
import base64
import http.client
import json
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

# Alias for current messages
messages = st.session_state.conversations[st.session_state.current_chat]["messages"]

def get_news_data(query="Football", limit=10, country="US", lang="en"):
    try:
        conn = http.client.HTTPSConnection("real-time-news-data.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "18ae1dcbd7msh2ea8bbe72ababffp15ea19jsn1f769e59c37e",
            'x-rapidapi-host': "real-time-news-data.p.rapidapi.com"
        }

        conn.request("GET", f"/search?query={query}&limit={limit}&time_published=anytime&country={country}&lang={lang}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))

        # Format the news data nicely
        articles = data.get("data", [])
        if not articles:
            return "No news found for that topic."

        news_list = []
        for article in articles[:limit]:
            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown Source")
            link = article.get("link", "#")
            news_list.append(f"📰 **{title}**  \n📍 *{source}*  \n🔗 [Read more]({link})\n")

        return "\n\n".join(news_list)

    except Exception as e:
        return f"⚠️ Error fetching news: {str(e)}"


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
        {"role": "system", "content": "You are LlamaBuddy, an AI assistant powered by LLaMA 3. You can chat naturally, generate code, translate text to English, explain concepts in simple terms, summarize text, rewrite text, brainstorm ideas, fetch weather data using the get_weather_data function, and handle various other tasks. Respond appropriately based on the user's request. For code generation, provide executable code. For translations, provide the translated text. For explanations, keep it simple. For weather queries, use the get_weather_data function with lat, lon (optional start_date, end_date for historical data). Always be helpful and accurate."}
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

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def get_weather_data(lat, lon, start_date=None, end_date=None):
    try:
        conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "18ae1dcbd7msh2ea8bbe72ababffp15ea19jsn1f769e59c37e",
            'x-rapidapi-host': "meteostat.p.rapidapi.com"
        }
        if start_date and end_date:
            # For historical or range data, use monthly
            conn.request("GET", f"/point/monthly?lat={lat}&lon={lon}&alt=43&start={start_date}&end={end_date}", headers=headers)
        else:
            # For today's weather, use daily with today's date
            today = datetime.now().strftime("%Y-%m-%d")
            conn.request("GET", f"/point/daily?lat={lat}&lon={lon}&alt=43&start={today}&end={today}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(page_title="LlamaBuddy - AI Assistant", page_icon="🦙")
st.title("🦙 LlamaBuddy")
st.markdown("*Your intelligent AI assistant powered by LLaMA 3*")


# Theme selection
if "theme" not in st.session_state:
    st.session_state.theme = "light"
dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.theme == "Dark")
st.session_state.theme = "Dark" if dark_mode else "Light"

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
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stTextInput > div > div > input {
            background-color: #1f2937;
            color: white;
            border-color: #374151;
            border-radius: 20px;
            padding: 10px;
        }
        .stButton > button {
            background-color: #374151;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #4b5563;
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
            border-radius: 10px;
        }
        .stMarkdown h1 {
            color: #60a5fa;
        }
        .stMarkdown p {
            color: #d1d5db;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stTextInput > div > div > input {
            border-radius: 20px;
            padding: 10px;
        }
        .stButton > button {
            border-radius: 10px;
            border: none;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #e5e7eb;
        }
        .stMarkdown h1 {
            color: #1f2937;
        }
    </style>
    """, unsafe_allow_html=True)

# The AI can handle various tasks automatically based on your prompt.
# For example: "Translate this text", "Explain quantum physics", "Write Python code for a calculator"

st.sidebar.header("💬 Chats")
for i, conv in enumerate(st.session_state.conversations):
    if st.sidebar.button(f"Chat {conv['id']}", key=f"chat_{i}"):
        st.session_state.current_chat = i
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Chat Management")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("➕ New Chat"):
        new_id = len(st.session_state.conversations) + 1
        st.session_state.conversations.append({"id": new_id, "messages": [{"role": "assistant", "content": "How can I help you today?"}]})
        st.session_state.current_chat = len(st.session_state.conversations) - 1
        st.rerun()

with col2:
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.conversations[st.session_state.current_chat]["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]
        st.rerun()

# Display chat history
for i, message in enumerate(messages):
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['role'].capitalize()}** - {datetime.now().strftime('%H:%M')}")
        if "```" in message["content"]:
            st.code(message["content"], language="python")
        else:
            st.write(message["content"])
    if message["role"] == "assistant":
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🎤 Voice Reply", key=f"voice_reply_{i}"):
                recognizer = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    st.info("🎙️ Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                try:
                    text = recognizer.recognize_google(audio)
                    st.success(f"✅ Transcribed: {text}")
                    prompt = text
                    messages.append({"role": "user", "content": prompt})
                    with st.spinner("🤖 Generating response..."):
                        response = get_llama_response(messages)
                    if response:
                        messages.append({"role": "assistant", "content": response})
                    else:
                        st.warning("⚠️ Failed to get response. Please check your API key and try again.")
                except sr.UnknownValueError:
                    st.error("❌ Could not understand the audio")
                except sr.RequestError as e:
                    st.error(f"❌ Speech recognition error: {e}")
        with col2:
            if st.button("🔊 Speak", key=f"speak_{i}"):
                audio_buffer = text_to_speech(message["content"])
                if audio_buffer:
                    audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode()
                    audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
                    st.markdown(audio_html, unsafe_allow_html=True)



# User input
st.markdown("---")
if prompt := st.chat_input("💬 Ask me anything... (e.g., 'Explain quantum physics' or 'Write a Python function')"):
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Generating response..."):
            response = get_llama_response(messages)

        if response:
            if "```" in response:
                st.code(response, language="python")
            else:
                st.write(response)
            messages.append({"role": "assistant", "content": response})
        else:
            st.warning("⚠️ Failed to get response. Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: small;">
    <p>🦙 LlamaBuddy v1.0 | Powered by LLaMA 3 & OpenRouter</p>
    
</div>
""", unsafe_allow_html=True)
