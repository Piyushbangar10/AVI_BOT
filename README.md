# AVI BOT - AI Assistant

AVI BOT is a comprehensive AI-powered personal assistant designed to automate tasks, provide information, and control system functions through voice and text interactions. It features a modern web-based user interface and integrates with Ollama for intelligent responses.

## Developers
*   **Piyush Bangar**
*   **Yash Verma**


## Features

### Intelligence & Interaction
*   **Voice & Text Interaction**: Supports speech-to-text and text-to-speech for seamless communication.
*   **AI Backend**: Integrates with **Ollama** (Llama 3) for advanced conversational capabilities.
*   **Intent Recognition**: Uses TF-IDF and Cosine Similarity to understand user commands locally.

### System Automation
*   **System Controls**: Adjust volume, brightness, lock screen, shutdown, and restart the PC.
*   **App Management**: Open and close applications effortlessly.
*   **System Monitoring**: Real-time tracking of CPU usage, RAM, and Battery status.
*   **System Storage**: Check disk usage and free space.

### Productivity & Tools
*   **Weather Updates**: Get real-time weather information for any city (auto-detects location).
*   **News Headlines**: Fetches the top 5 latest news headlines.
*   **Note Taking**: Dictate notes to save them for later and have them read back to you.
*   **Wikipedia & Google Search**: instant information retrieval from the web.
*   **WhatsApp Automation**: Send WhatsApp messages hands-free.
*   **Screen Capture**: Take screenshots with a simple command.

### Entertainment
*   **YouTube Integration**: Open YouTube, search for videos, or play music on YouTube Music.

## specialized Modules
*   `news.py`: Handles fetching news data.
*   `weather.py`: Interface for Open-Meteo API to get weather data.
*   `notes_manager.py`: Manages saving and retrieving local notes.
*   `web/`: Contains the frontend web interface (HTML/JS/CSS).

## Requirements
*   Python 3.x
*   Ollama (running locally)
*   Required Python packages (see imports in `main.py`): `eel`, `speech_recognition`, `pyttsx3`, `pywhatkit`, `pyautogui`, `requests`, `psutil`, `screen_brightness_control`, `AppOpener`, `scikit-learn`, `wikipedia`.

## Usage
Run the main script to start the assistant and the web interface:
```bash
python main.py
```
