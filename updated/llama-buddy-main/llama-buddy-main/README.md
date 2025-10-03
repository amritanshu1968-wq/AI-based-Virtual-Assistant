# 🦙 LlamaBuddy – Streamlit AI Assistant

An interactive chatbot powered by **Meta’s LLaMA 3 (70B)** via **OpenRouter**, built with **Streamlit**.  
Supports chat, code generation, language translation, and explanation — all in one sleek interface!

![LlamaBuddy Preview](preview.png)

---

## 🚀 Features

- 💬 **Chat** mode (natural conversation)
- 👨‍💻 **Code generation** with syntax highlighting
- 🌍 **Translate** any input to English
- 📖 **Explain** complex topics in simple terms
- ⏳ API rate limit handling (10s)

---

## 🧠 Tech Stack

| Tool        | Purpose                 |
|-------------|--------------------------|
| `Streamlit` | Interactive UI / Chat   |
| `OpenRouter`| Access LLaMA-3 via API  |
| `Python`    | Backend logic           |
| `Requests`  | API communication       |

---

## 🌐 Deployment

### Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run LlamaBuddy.py`
3. Open the provided URL in your browser.

### Deploy to Streamlit Cloud

1. Fork or clone this repository to your GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and sign in with GitHub.
3. Click "New app" and select your repository.
4. Set the main file path to `LlamaBuddy.py`.
5. In the app settings, add your OpenRouter API key as a secret:
   - Key: `API_KEY`
   - Value: Your OpenRouter API key
6. Deploy the app.

### Other Deployment Options

- **Heroku**: Use the Streamlit buildpack.
- **AWS/GCP/Azure**: Deploy as a containerized app.

For more details, refer to the [Streamlit documentation](https://docs.streamlit.io/).

---

