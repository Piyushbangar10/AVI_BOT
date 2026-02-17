import eel
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui
import os
import json
import random
import time
import queue # Added queue
import datetime
import webbrowser
import psutil
import requests
import screen_brightness_control as sbc
from AppOpener import open as app_open, close as app_close
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ctypes
import shutil
import weather
import news
import notes_manager
import wikipedia

# --- INIT EEL ---
eel.init('web')

# --- CONFIGURATION ---
speech_lock = threading.Lock()
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
SYSTEM_PERSONA = "You are Avi, a helpful AI assistant. Keep answers short (max 2 sentences) and witty."

# --- VOICE ENGINE ---
# --- VOICE ENGINE ---
speech_queue = queue.Queue()

def tts_worker():
    """Worker thread to handle speech serially and safely"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        engine.setProperty('rate', 170)
        
        while True:
            text = speech_queue.get()
            if text is None: break # Poison pill
            try:
                engine.say(text)
                engine.runAndWait()
            except: pass
            speech_queue.task_done()
    except Exception as e:
        print(f"TTS Engine Crash: {e}")

# Start the worker immediately
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    print(f"AVI: {text}")
    eel.updateTerminal(text, "avi") 
    # Non-blocking add to queue
    speech_queue.put(text)

# --- INTELLIGENCE ---
class AviBrain:
    def __init__(self):
        self.vectorizer = None
        self.X = None
        self.tags = []
        self.intents_data = {}
        self.train()

    def train(self):
        if os.path.exists('intents.json'):
            with open('intents.json', 'r') as f:
                self.intents_data = json.load(f)
            corpus = []
            self.tags = []
            for intent in self.intents_data['intents']:
                for pattern in intent['patterns']:
                    corpus.append(pattern)
                    self.tags.append(intent['tag'])
            self.vectorizer = TfidfVectorizer()
            self.X = self.vectorizer.fit_transform(corpus)
        else:
            print("Error: intents.json missing.")

    def get_intent(self, query):
        if not self.vectorizer: return "unknown"
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.X)
        best_match = similarities.argmax()
        confidence = similarities[0][best_match]
        if confidence < 0.4: return "unknown"
        return self.tags[best_match]

    def ask_ollama(self, query):
        eel.updateStatus("Thinking...")
        try:
            # Memory Context
            memory_context = ""
            if os.path.exists('jarvis_memory.json'):
                try:
                    with open('jarvis_memory.json', 'r') as f:
                        mem = json.load(f)
                        # Get last 3 turns
                        recent = mem[-3:] if len(mem) > 3 else mem
                        for turn in recent:
                            memory_context += f"{turn['role']}: {turn['content']}\n"
                except: pass
            
            final_prompt = f"System: {SYSTEM_PERSONA}\nContext: {memory_context}\nUser: {query}"
            
            data = {
                "model": OLLAMA_MODEL,
                "prompt": final_prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_URL, json=data)
            if response.status_code == 200:
                answer = response.json()['response']
                # Save to memory logic could go here
                return answer
            return "I couldn't think of an answer."
        except: return "My brain is offline."

# --- HARDWARE & AUTOMATION ---
class HardwareController:
    @staticmethod
    def take_screenshot():
        """Captures screen and saves with timestamp"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return "Failed to take screenshot."

    @staticmethod
    def send_whatsapp_logic(name, message):
        """Automates WhatsApp Desktop"""
        speak(f"Sending message to {name}...")
        try:
            app_open("WhatsApp", match_closest=True, output=False)
        except:
            speak("I couldn't find WhatsApp.")
            return

        time.sleep(2) 
        
        # Search Contact
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyautogui.write(name)
        time.sleep(1.0)
        
        # Select Contact
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Send Message
        pyautogui.write(message)
        time.sleep(0.5)
        pyautogui.press('enter')
        speak("Message sent.")

    @staticmethod
    def open_application(app_name):
        try:
            app_open(app_name, match_closest=True, output=False)
            return f"Opening {app_name}."
        except:
            return f"I could not find {app_name}."

# --- MAIN LISTENING LOOP ---
brain = AviBrain()
hw = HardwareController()
is_listening = False

def listen_once(recognizer, source):
    """Sub-listener for details like names/messages"""
    try:
        eel.updateStatus("Listening for detail...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        text = recognizer.recognize_google(audio).lower()
        eel.updateTerminal(text, "user")
        return text
    except:
        return None

@eel.expose
def start_avi():
    global is_listening
    if is_listening: return
    is_listening = True
    t = threading.Thread(target=run_listening_loop)
    t.daemon = True
    t.start()
    
    # Start Monitor Thread
    m = threading.Thread(target=monitor_system)
    m.daemon = True
    m.start()

    # Weather thread starts on app_ready signal now


def monitor_system():
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            battery = psutil.sensors_battery()
            batt_percent = battery.percent if battery else 100
            eel.updateStats(cpu, ram, batt_percent)
            time.sleep(2)
        except:
            time.sleep(2)

@eel.expose
def app_ready():
    """Called by JS when the UI is fully loaded"""
    print("UI Ready Signal Received.")
    # Trigger weather check now
    threading.Thread(target=initial_weather_check, daemon=True).start()

def initial_weather_check():
    """Fetches weather for default location"""
    # No sleep needed, triggered by app_ready
    try:
        # Auto-detect location
        city = weather.get_system_location()
        data = weather.get_weather_data(city)
        if not data.get("error"):
            cond = "Clear" # default
            code = data.get('weathercode', 0)
            # simple mapping
            if code in [0]: cond = "Sunny"
            elif code in [1,2,3]: cond = "Cloudy"
            elif code in [45,48]: cond = "Foggy"
            elif code >= 51: cond = "Rain"
            
            eel.updateWeather(data['temp'], cond, data['city'])
    except Exception as e:
        print(f"Weather Init Error: {e}")

def run_listening_loop():
    speak("Systems Online.")
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.6
    
    # OPTIMIZATION: One-time adjustment
    with sr.Microphone() as source:
        eel.updateStatus("Calibrating...")
        r.adjust_for_ambient_noise(source, duration=1)
        eel.updateStatus("Ready")

    while True:
        eel.updateStatus("Listening...")
        with sr.Microphone() as source:
            try:
                # No re-adjustment here = Faster response
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                eel.updateStatus("Processing...")
                query = r.recognize_google(audio).lower()
                eel.updateTerminal(query, "user")

                # --- 1. OPEN APP OVERRIDE ---
                if query.startswith("open ") and "youtube" not in query:
                    app_name = query.replace("open", "").strip()
                    speak(hw.open_application(app_name))
                    continue

                # --- 2. INTENT CHECK ---
                tag = brain.get_intent(query)

                # --- 3. COMMAND EXECUTION ---
                
                # *** SCREENSHOT ***
                if tag == "screenshot" or "screenshot" in query:
                    speak("Capturing screen.")
                    result = hw.take_screenshot()
                    speak(result)

                # *** SYSTEM CONTROLS ***
                elif tag == "volume_up":
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    speak("Volume increased.")
                
                elif tag == "volume_down":
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    speak("Volume decreased.")
                
                elif tag == "brightness_up":
                    try:
                        current = sbc.get_brightness()
                        # handle if list or single int
                        if isinstance(current, list): current = current[0]
                        new_val = min(current + 10, 100)
                        sbc.set_brightness(new_val)
                        speak("Brightness increased.")
                    except: speak("Could not adjust brightness.")
                
                elif tag == "brightness_down":
                    try:
                        current = sbc.get_brightness()
                        if isinstance(current, list): current = current[0]
                        new_val = max(current - 10, 0)
                        sbc.set_brightness(new_val)
                        speak("Brightness decreased.")
                    except: speak("Could not adjust brightness.")

                elif tag == "lock_system":
                    speak("Locking system.")
                    ctypes.windll.user32.LockWorkStation()
                
                elif tag == "minimize_windows":
                    pyautogui.hotkey('win', 'd')
                    speak("Windows minimized.")

                elif tag == "shutdown_system":
                    speak("Initiating shutdown sequence.")
                    os.system("shutdown /s /t 5")

                elif tag == "restart_system":
                    speak("Restarting system.")
                    os.system("shutdown /r /t 5")
                
                elif tag == "google_search":
                    speak("What should I search for?")
                    with sr.Microphone() as src:
                        r.adjust_for_ambient_noise(src, duration=0.5)
                        search_q = listen_once(r, src)
                    if search_q:
                        speak(f"Searching Google for {search_q}")
                        os.startfile(f"https://google.com/search?q={search_q}")
                    else:
                        speak("I didn't hear anything.")

                elif tag == "date_time":
                    now = datetime.datetime.now()
                    if "time" in query:
                         time_str = now.strftime("%I:%M %p")
                         speak(f"The time is {time_str}")
                    elif "date" in query:
                        date_str = now.strftime("%A, %B %d, %Y")
                        speak(f"Today is {date_str}")
                    else:
                        date_str = now.strftime("%A, %B %d")
                        time_str = now.strftime("%I:%M %p")
                        speak(f"It is {time_str}, on {date_str}.")

                elif tag == "battery_status":
                    batt = psutil.sensors_battery()
                    if batt:
                        speak(f"Battery is at {batt.percent} percent.")
                    else:
                        speak("Cannot read battery status.")
                
                elif tag == "cpu_status":
                    cpu = psutil.cpu_percent()
                    speak(f"CPU usage is at {cpu} percent.")

                # *** NEW EXPANDED FEATURES ***
                elif tag == "weather":
                    speak("Which city?")
                    with sr.Microphone() as src:
                        r.adjust_for_ambient_noise(src, duration=0.5)
                        city = listen_once(r, src)
                    if city:
                        speak("Checking weather...")
                        data = weather.get_weather_data(city)
                        if not data.get("error"):
                            # Logic to map code to text for speech
                            cond = "Clear" # default
                            code = data.get('weathercode', 0)
                            if code in [0]: cond = "Sunny"
                            elif code in [1,2,3]: cond = "Cloudy"
                            elif code in [45,48]: cond = "Foggy"
                            elif code >= 51: cond = "Rain"
                            
                            eel.updateWeather(data['temp'], cond, data['city'])
                            speak(f"Current weather in {data['city']}: {data['temp']} degrees, {cond}.")
                        else:
                             speak(data['error'])
                    else:
                        speak("I didn't hear a city name.")

                elif tag == "news":
                    speak("Fetching top headlines.")
                    headlines = news.get_news(limit=5)
                    if headlines:
                        for i, head in enumerate(headlines, 1):
                            speak(f"{i}. {head}")
                    else:
                        speak("I couldn't fetch the news right now.")

                elif tag == "take_note":
                    speak("What should I write down?")
                    with sr.Microphone() as src:
                        r.adjust_for_ambient_noise(src, duration=0.5)
                        note_text = listen_once(r, src)
                    if note_text:
                        res = notes_manager.add_note(note_text)
                        speak(res)
                    else:
                        speak("I didn't hear anything to note.")

                elif tag == "read_notes":
                    notes = notes_manager.read_notes()
                    speak(notes)

                elif tag == "system_status_extended":
                    total, used, free = shutil.disk_usage("/")
                    total_gb = total // (2**30)
                    used_gb = used // (2**30)
                    free_gb = free // (2**30)
                    speak(f"System Storage: {used_gb} GB used out of {total_gb} GB. {free_gb} GB free.")

                # *** NEW FEATURES ***
                elif tag == "wikipedia_search":
                    speak("Searching Wikipedia...")
                    query_clean = query.replace("who is","").replace("what is","").replace("tell me about","").replace("wikipedia","").strip()
                    try:
                        results = wikipedia.summary(query_clean, sentences=2)
                        speak(results)
                    except wikipedia.exceptions.DisambiguationError:
                        speak("There are many results. Opening Google.")
                        os.startfile(f"https://google.com/search?q={query_clean}")
                    except wikipedia.exceptions.PageError:
                        speak("I couldn't find a direct match. searching Google.")
                        os.startfile(f"https://google.com/search?q={query_clean}")
                    except Exception:
                        speak("Could not fetch data. Searching Google.")
                        os.startfile(f"https://google.com/search?q={query_clean}")
                
                elif tag == "close_app":
                    app_to_close = query.replace("close", "").replace("exit", "").strip()
                    speak(f"Closing {app_to_close}")
                    try:
                        app_close(app_to_close, match_closest=True, output=False)
                    except:
                        # Fallback for some system apps if AppOpener fails
                        proc_name = app_to_close.replace(" ", "") + ".exe"
                        os.system(f"taskkill /f /im {proc_name}")

                elif tag == "type_text":
                    text_to_type = query.replace("type", "").replace("write this", "").strip()
                    speak("Typing.")
                    pyautogui.write(text_to_type)
                
                elif tag == "stop_listening":
                    speak("Pausing. Say 'Wake up' to resume.")
                    # Simple blocking wait loop
                    while True:
                         with sr.Microphone() as src2:
                            try:
                                audio2 = r.listen(src2, timeout=5, phrase_time_limit=5)
                                txt = r.recognize_google(audio2).lower()
                                if "wake up" in txt:
                                    speak("Online.")
                                    break
                            except: pass

                # *** WHATSAPP ***
                elif tag == "send_whatsapp" or "send whatsapp" in query:
                    speak("Who is the message for?")
                    with sr.Microphone() as sub_source:
                        r.adjust_for_ambient_noise(sub_source, duration=0.5)
                        name = listen_once(r, sub_source)
                    
                    if name:
                        speak(f"What is the message for {name}?")
                        with sr.Microphone() as sub_source:
                            r.adjust_for_ambient_noise(sub_source, duration=0.5)
                            msg = listen_once(r, sub_source)
                        
                        if msg:
                            hw.send_whatsapp_logic(name, msg)
                        else:
                            speak("I didn't hear a message. Cancelling.")
                    else:
                        speak("I didn't hear a name. Cancelling.")

                # *** MEDIA / OTHER ***
                elif tag == "unknown":
                    reply = brain.ask_ollama(query)
                    speak(reply)
                
                elif tag == "youtube":
                    os.startfile("https://youtube.com")
                    speak("Opening YouTube.")
                
                elif tag == "youtube_music":
                    os.startfile("https://music.youtube.com")
                    speak("Playing Music.")
                
                elif tag == "bye":
                    speak("Goodbye.")
                    os._exit(0)
                
                elif "play" in query and "youtube" in query:
                    song = query.replace("play", "").replace("on youtube", "").strip()
                    speak(f"Playing {song}")
                    pywhatkit.playonyt(song)
                
                else:
                    for intent in brain.intents_data['intents']:
                        if intent['tag'] == tag:
                            speak(random.choice(intent['responses']))
                            break

            except Exception as e:
                pass

eel.start('index.html', size=(700, 900))