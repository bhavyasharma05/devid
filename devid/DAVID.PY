import requests
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import random
import os
import subprocess
import time
import webbrowser
from bs4 import BeautifulSoup  # Import for web scraping
import nltk  # Natural Language Toolkit
import pyautogui  # For task automation
try:
    import psutil
except ImportError:
    print("psutil module not found. Please install it using 'pip install psutil'.")
    psutil = None

SPEECH_RATE = 150  # Speech rate
RESPONSE_DELAY = 0.5  # Pause before answering
#engine = pyttsx3.init()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set. Please set it as an environment variable.")
    exit()

class Devid:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', SPEECH_RATE)
        self.last_command_time = time.time()

    def speak(self, text):
        """Speak the text with a slight delay for smooth interaction."""
        time.sleep(RESPONSE_DELAY)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for user commands."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized Command: {command}")
                return command
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                return None
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return None
            except sr.RequestError as e:
                print(f"Request Error: {e}")
                self.speak("I am having trouble connecting to the internet. Please check your connection.")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    def _run_application(self, app_name, action):
        """Helper function to run or close applications."""
        try:
            if "notepad" in app_name:
                app_executable = "notepad.exe"
                app_friendly_name = "Notepad"
            elif "chrome" in app_name:
                app_executable = "chrome.exe"
                app_friendly_name = "Google Chrome"
            else:
                self.speak("I couldn't find the application.")
                return

            if action == "open":
                self.speak(f"Opening {app_friendly_name}.")
                subprocess.run([app_executable.replace(".exe", "")], check=True)
            elif action == "close":
                self.speak(f"Closing {app_friendly_name}.")
                if psutil:
                    for proc in psutil.process_iter(['name']):
                        if proc.info['name'] == app_executable:
                            proc.kill()
                            break
                else:
                    self.speak("The 'psutil' module is not available, so I cannot close the application.")
        except subprocess.CalledProcessError as e:
            self.speak(f"Error {action}ing application: Could not {action} {app_friendly_name}. Error: {e}")
        except Exception as e:
            self.speak(f"Error {action}ing application: An unexpected error occurred while trying to {action} {app_friendly_name}. Error: {e}")

    def open_application(self, app_name):
        """Open specific applications."""
        self._run_application(app_name, "open")

    def close_application(self, app_name):
        """Close specific applications."""
        self._run_application(app_name, "close")

    def send_whatsapp_message(self, contact, message):
        """Send a WhatsApp message using WhatsApp Web (placeholder for actual API)."""
        self.speak(f"Sending your message to {contact}: {message}")
        webbrowser.open(f"https://wa.me/{contact}?text={message}")

    def manage_gmail(self, action):
        """Gmail management (placeholder for actual Gmail API integration)."""
        if action == "check unread emails":
            self.speak("You have 5 unread emails.")
        elif action == "clear spam":
            self.manage_gmail("clear spam")

    def connect_bluetooth(self, device_name):
        """Connect to a Bluetooth device (placeholder for actual implementation)."""
        self.speak(f"Connecting to Bluetooth device: {device_name}")

    def connect_wifi(self, network_name):
        """Connect to a WiFi network (placeholder for actual implementation)."""
        self.speak(f"Connecting to WiFi network: {network_name}")

    def recognize_intent(self, command):
        """Placeholder for intent recognition."""
        # Use NLTK or other NLP libraries to determine the user's intent
        self.speak("Recognizing intent...")
        try:
            from nltk.tokenize import word_tokenize
            tokens = word_tokenize(command)
            print(f"Tokens: {tokens}")
            return "unknown"
        except Exception as e:
            print(f"Error in recognize_intent: {e}")
            return "unknown"

    def extract_entities(self, command):
        """Placeholder for entity extraction."""
        # Use NLTK or other NLP libraries to extract entities from the command
        self.speak("Extracting entities...")
        return {}

    def create_folder(self, folder_name, location):
        """Placeholder for task automation: create a folder."""
        self.speak(f"Creating folder {folder_name} at {location}...")

    def recommend_restaurant(self, location):
        """Placeholder for AI-driven recommendations: recommend a restaurant."""
        self.speak(f"Recommending a restaurant in {location}...")
        return "Some Restaurant"

    def set_reminder(self, time, task):
        """Placeholder for smart notifications: set a reminder."""
        self.speak(f"Setting a reminder for {time} to {task}...")

    def learn_user_preferences(self, command):
        """Placeholder for machine learning-based user behavior adaptation."""
        self.speak("Learning user preferences...")

    def query_gemini(self, prompt):
        """Dynamic question answering through Gemini API with web scraping fallback."""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)  # Add timeout
            if response.status_code == 200:
                data = response.json()
                answer = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                return answer.strip()
            else:
                return f"Error: {response.status_code}. Unable to fetch the answer."
        except requests.exceptions.Timeout:
            print("Gemini API timed out. Falling back to web scraping...")
            return self.scrape_answer(prompt)
        except Exception as e:
            print(f"Error connecting to Gemini API: {e}")
            return "Sorry, I couldn't connect to the answer service."

    def scrape_answer(self, prompt):
        """Scrape answer from a search engine (e.g., Google)."""
        try:
            search_url = f"https://www.google.com/search?q={prompt}"
            response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')
            answer = soup.find('div').text  # Extract answer from Google's knowledge panel
            print(f"Extracted answer: {answer}")
            return answer.strip()
        except requests.exceptions.RequestException as e:
            print(f"Error during web scraping: {e}")
            return "I am unable to fetch the answer from the internet."
        except AttributeError:
            print("Answer not found in the scraped content.")
            return "I couldn't find a direct answer on the web."

    def process_command(self, command):
        """Process user commands."""
        self.last_command_time = time.time()

        if "time" in command:
            self.speak(datetime.now().strftime("The time is %H:%M."))
        elif "joke" in command:
            self.speak(random.choice([
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!"
            ]))
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            self.open_application(app_name)
        elif "close" in command:
            app_name = command.replace("close", "").strip()
            self.close_application(app_name)
        elif "send a message on whatsapp":
            contact = "1234567890"
            message = "Hello, how are you?"
            self.send_whatsapp_message(contact, message)
        elif "check unread emails":
            self.manage_gmail("check unread emails")
        elif "clear spam":
            self.manage_gmail("clear spam")
        elif "connect bluetooth":
            device_name = command.replace("connect bluetooth with", "").strip()
            self.connect_bluetooth(device_name)
        elif "connect wifi":
            network_name = command.replace("connect to wifi", "").strip()
            self.connect_wifi(network_name)
        elif "sto" in command:
            self.engine.stop()
            self.speak("I have stopped. Listening...")
            return None
        elif "exit" in command:
            self.speak("Goodbye!")
            return "Goodbye!"
        else:
            # NLP functionalities (intent recognition, entity extraction)
            # Example: "set a reminder for tomorrow at 9am to buy groceries"
            # Placeholder for intent recognition
            intent = self.recognize_intent(command)
            # Placeholder for entity extraction
            entities = self.extract_entities(command)

            # Task automation
            # Example: "create a new folder named 'Project X' on my desktop"
            if intent == "create_folder":
                self.create_folder(entities["folder_name"], entities["location"])

            # AI-driven recommendations
            # Example: "recommend me a good restaurant nearby"
            if intent == "recommend_restaurant":
                restaurant = self.recommend_restaurant(entities["location"])
                self.speak(f"I recommend {restaurant} in {entities['location']}.")

            # Smart notifications
            # Example: "remind me to take a break in 30 minutes"
            if intent == "set_reminder":
                self.set_reminder(entities["time"], entities["task"])

            # Machine learning-based user behavior adaptation
            # Placeholder for learning user preferences and adapting behavior
            self.learn_user_preferences(command)

            response = self.query_gemini(command)
            if response:
                self.speak(response)

if __name__ == "__main__":
    devid = Devid()
    devid.speak("Hello! I’m Devid. How can I assist you today?")
    while True:
        command = devid.listen()
        if command:
            if "devid" in command:
                command = command.replace("devid", "").strip()
                devid.speak("Yes Sir?")
                response = devid.process_command(command)
                if response == "Goodbye!":
                    break
                elif response:
                    devid.speak(response)
            else:
                response = devid.process_command(command)
                if response == "Goodbye!":
                    break
                elif response:
                    devid.speak(response)
        else:
            if time.time() - devid.last_command_time > 10:
                devid.speak("Going to sleep. Call me 'Devid' to wake me up.")
                devid.last_command_time = time.time()
                while True:
                    wake_up = devid.listen()
                    if wake_up and "devid" in wake_up:
                        devid.speak("I'm awake. How can I help you?")
                        break
                    time.sleep(1)
