import requests
import json
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import random
import os
import subprocess
import time
import webbrowser


engine = pyttsx3.init()


SPEECH_RATE = 150  # Speech rate
RESPONSE_DELAY = 0.5  # Pause before answering
engine.setProperty('rate', SPEECH_RATE)


OPENROUTER_API_KEY = "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"


last_command_time = time.time()

def speak(text):
    """Speak the text with a slight delay for smooth interaction."""
    time.sleep(RESPONSE_DELAY)
    engine.say(text)
    engine.runAndWait()

def listen():
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
            speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def open_application(app_name):
    """Open specific applications."""
    if "notepad" in app_name:
        speak("Opening Notepad.")
        os.system("notepad")
    elif "chrome" in app_name:
        speak("Opening Google Chrome.")
        subprocess.run(["start", "chrome"], shell=True)
    elif "youtube" in app_name:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    else:
        speak("I couldn't find the application.")

def close_application(app_name):
    """Close specific applications."""
    if "notepad" in app_name:
        speak("Closing Notepad.")
        os.system("taskkill /f /im notepad.exe")
    elif "chrome" in app_name:
        speak("Closing Google Chrome.")
        os.system("taskkill /f /im chrome.exe")
    else:
        speak("I couldn't find the application to close.")

def send_whatsapp_message(contact, message):
    """Send a WhatsApp message using WhatsApp Web (placeholder for actual API)."""
    speak(f"Sending your message to {contact}: {message}")
    webbrowser.open(f"https://wa.me/{contact}?text={message}")

def manage_gmail(action):
    """Gmail management (placeholder for actual Gmail API integration)."""
    if action == "check unread emails":
        speak("You have 5 unread emails.")  # Replace with actual Gmail API call
    elif action == "clear spam":
        speak("Clearing all spam emails.")  # Replace with actual Gmail API call

def connect_bluetooth(device_name):
    """Connect to a Bluetooth device (placeholder for actual implementation)."""
    speak(f"Connecting to Bluetooth device: {device_name}")
   

def connect_wifi(network_name):
    """Connect to a WiFi network (placeholder for actual implementation)."""
    speak(f"Connecting to WiFi network: {network_name}")
  

def query_openrouter(prompt):
    """Dynamic question answering through OpenRouter API."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant. Provide concise answers to user questions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return answer.strip()
        else:
            return f"Error: {response.status_code}. Unable to fetch the answer."
    except Exception as e:
        print(f"Error connecting to OpenRouter API: {e}")
        return "Sorry, I couldn't connect to the answer service."

def process_command(command):
    """Process user commands."""
    global last_command_time
    last_command_time = time.time()  # Reset command timer

    if "time" in command:
        return datetime.now().strftime("The time is %H:%M.")
    elif "joke" in command:
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta!",
        ])
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    elif "close" in command:
        app_name = command.replace("close", "").strip()
        close_application(app_name)
    elif "send a message on whatsapp" in command:
        contact = "1234567890"  # Replace with dynamic contact logic
        message = "Hello, how are you?"  # Replace with dynamic message logic
        send_whatsapp_message(contact, message)
    elif "check unread emails" in command:
        manage_gmail("check unread emails")
    elif "clear spam" in command:
        manage_gmail("clear spam")
    elif "connect bluetooth" in command:
        device_name = command.replace("connect bluetooth with", "").strip()
        connect_bluetooth(device_name)
    elif "connect wifi" in command:
        network_name = command.replace("connect to wifi", "").strip()
        connect_wifi(network_name)
    elif "stop" in command or "exit" in command:
        return "Goodbye!"
    else:
        return query_openrouter(command)

if __name__ == "__main__":
    speak("Hello! I’m Devid. How can I assist you today?")
    while True:
        command = listen()
        if command:
            response = process_command(command)
            if response:
                speak(response)
                if response == "Goodbye!":
                    break
        elif time.time() - last_command_time > 10:
            speak("Good to have you here, Sir!")
            last_command_time = time.time()
