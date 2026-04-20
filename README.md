# 🤖 AVI BOT - AI Desktop Voice Assistant

AVI BOT is a **Jarvis-like AI-powered desktop assistant** designed to automate tasks, provide intelligent responses, and interact with users through **voice and text**. It combines AI, system automation, and a modern web-based UI to deliver a powerful personal assistant experience.

---

## 🧠 What This Project Is

AVI BOT is a **Desktop Voice Assistant**, not a web app or chatbot alone.

### Key Capabilities:

* 🎤 Voice Input (Speech Recognition)
* 🔊 Voice Output (Text-to-Speech)
* 🧠 AI-powered responses (Hybrid: Intent + LLM)
* 🖥️ System Control & Automation
* 🌐 Web-based User Interface (via Eel)

---

## 🧩 Tech Stack Overview

### 🐍 Core Language

* Python (Main backend logic)

  * Files: `main.py`, `weather.py`, `news.py`, etc.

---

### 🧠 AI / NLP Layer

* Intent-based chatbot using `intents.json`
* TF-IDF + Cosine Similarity (via scikit-learn)
* LLM fallback using Ollama (Llama 3)

👉 Hybrid system:

* Rule-based (fast & local)
* LLM-based (flexible & intelligent)

---

### 🎤 Voice Input

* `speech_recognition`
* Google Speech API (`recognize_google`)

---

### 🔊 Voice Output

* `pyttsx3` (offline text-to-speech engine)

---

### 🖥️ System Automation

* `pyautogui` → keyboard & mouse control
* `ctypes` → Windows system functions
* `os` → shutdown/restart
* `psutil` → CPU, RAM, battery monitoring
* `screen_brightness_control` → brightness control

---

### 🌐 Backend ↔ Frontend Bridge

* `eel`

  * Connects Python backend with web frontend
  * Enables real-time interaction between JS and Python

---

### 🎨 Frontend (UI)

Located in `/web/` folder:

* HTML (`index.html`)
* CSS (`style.css`)
* JavaScript (`script.js`)

#### Features:

* Terminal-style interface
* Live system stats (CPU, RAM, Battery)
* Weather display
* Animated typing responses

---

### 🌍 APIs Used

* 🌦️ Open-Meteo API → Weather data
* 📰 Google News RSS → Latest headlines
* 📍 IP API → Location detection

---

### 🗄️ Storage

* JSON Files:

  * `intents.json` → chatbot training data
  * `jarvis_memory.json` → assistant memory

* Text File:

  * `notes.txt` → saved notes

👉 No external database used

---

### 🧰 Additional Libraries

* `requests` → API calls
* `xml.etree.ElementTree` → RSS parsing
* `datetime`, `random`, `shutil`
* `wikipedia` → quick information

---

### 📱 Extra Integrations

* WhatsApp automation
* YouTube automation (`pywhatkit.playonyt`)
* Screenshot capture

---

## 🧱 Architecture

```
🎤 Voice Input (SpeechRecognition)
        ↓
🧠 Python Core (Intent + AI + Logic)
        ↓
🤖 Actions (System / API / Automation)
        ↓
🌐 Eel Bridge
        ↓
💻 Web UI (HTML + JS)
        ↓
🔊 Voice Output (TTS)
```

---

## 🚀 Features

### 🧠 Intelligence & Interaction

* Voice & Text Interaction
* AI responses using Ollama (Llama 3)
* Intent recognition using TF-IDF

---

### 🖥️ System Automation

* Control volume, brightness
* Shutdown / Restart / Lock system
* Open & close applications
* Monitor CPU, RAM, Battery
* Check disk usage

---

### 🛠️ Productivity & Tools

* Weather updates (auto-detect location)
* Latest news headlines
* Note taking (save & recall)
* Wikipedia & Google search
* Screenshot capture

---

### 🎵 Entertainment

* YouTube search & playback
* Music via YouTube Music

---

## 📁 Project Structure

* `main.py` → Main assistant logic
* `weather.py` → Weather API handling
* `news.py` → News fetching module
* `notes_manager.py` → Notes handling
* `intents.json` → Chatbot training data
* `web/` → Frontend UI

---

## ⚙️ Requirements

* Python 3.x
* Ollama (running locally)

### Required Python Packages:

```
eel
speech_recognition
pyttsx3
pywhatkit
pyautogui
requests
psutil
screen_brightness_control
AppOpener
scikit-learn
wikipedia
```

---

## ▶️ Usage

Run the assistant:

```
python main.py
```

This will:

* Start the backend
* Launch the web UI
* Activate voice assistant

---

## 👨‍💻 Developer

* Piyush Bangar

---

## 💡 Key Insight

AVI BOT is a **complete desktop AI assistant system**, combining:

👉 AI + Voice + Automation + UI

It is:

* ❌ Not just a chatbot
* ❌ Not a web app
* ❌ Not a Telegram bot

It is a **full Jarvis-like desktop assistant built with Python**

---
