# 🦙 LlamaBuddy – Streamlit AI Assistant

An interactive chatbot powered by **Meta’s LLaMA 3 (70B)** via **OpenRouter**, built with **Streamlit**.  
Supports chat, code generation, language translation, explanations, and even **speech input** — all in one sleek interface!

![LlamaBuddy Preview](preview.png)

---

## 🚀 Features

- 💬 **Chat naturally** with an AI assistant
- 👨‍💻 **Generate code** with syntax highlighting
- 🌍 **Translate** any text into English
- 📖 **Explain** complex topics in simple terms
- 🎙️ **Speech-to-Text**: talk to the assistant using your microphone
- 🌓 **Light/Dark theme toggle**
- ⏳ Built-in API rate limit handling (10s)

---

## 🧠 Tech Stack

| Tool             | Purpose                        |
|------------------|--------------------------------|
| `Streamlit`      | Interactive UI / Chat frontend |
| `OpenRouter API` | Access to LLaMA-3 model        |
| `Python`         | Core backend logic             |
| `Requests`       | API communication              |
| `SpeechRecognition` | Voice input support         |

---

## 📂 Project Structure

```
.
├── LlamaBuddy.py        # Main Streamlit app
├── requirements.txt     # Python dependencies
├── secrets.toml         # Stores API key (not uploaded to GitHub)
├── LICENSE              # License file
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/LlamaBuddy.git
cd LlamaBuddy
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.streamlit/secrets.toml` file and add:
```toml
API_KEY = "your-openrouter-api-key"
```

### 4. Run the app
```bash
streamlit run LlamaBuddy.py
```

Open the provided URL in your browser.

---

## 🌐 Deployment

### Deploy on Streamlit Cloud
1. Fork this repo to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and sign in.
3. Create a new app, select this repo, and set the main file to `LlamaBuddy.py`.
4. In **App Settings → Secrets**, add:
   - Key: `API_KEY`
   - Value: Your OpenRouter API key
5. Deploy!

### Other Options
- **Heroku**: Use the Streamlit buildpack.
- **Docker / Cloud Providers**: Deploy on AWS, GCP, or Azure.

---

## 🛡️ License
This project is licensed under the [MIT License](LICENSE).

---

## ✨ Future Improvements
- 🔊 Text-to-Speech responses
- 📊 Conversation history export
- 🖼️ AI-powered image generation integration

 
Feel free to ⭐ this repo if you like it!
