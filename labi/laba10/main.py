import os
import json
import pyaudio
import pyttsx3
import requests
from vosk import Model, KaldiRecognizer
from random import randint, choice

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PROJECT_DIR, 'vosk-model-small-en-us-0.15')
current_character = None


def speak(text):
    print(f"Assistant: {text}")
    print()
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
    
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Работает")


def handle_command(cmd):
    global current_character
    
    if "random" in cmd:
        current_character = get_random_character()
        with open(os.path.join(PROJECT_DIR, 'character.json'), 'w') as json_file:
            json.dump(current_character, json_file, indent=4)
        speak(f'{current_character['name']}.')
    
    elif "save" in cmd:
        image_url = current_character['image']
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                with open(os.path.join(PROJECT_DIR, 'character_image.jpg'), 'wb') as img:
                    img.write(response.content)
            speak("Saved.")
        except TimeoutError:
            speak('Timeout Error.')
        except Exception as e:
            speak(f'Exception: {e}')
    
    elif "episode" in cmd:
        speak(f"First shown in episode {current_character['episode'][0].split('/')[-1]}.")
    
    elif "show" in cmd:
        try:
            os.startfile(os.path.join(PROJECT_DIR, 'character_image.jpg'))
        except Exception as e:
            speak(f'Exception: {e}')
            
    elif 'exit' in cmd:
        speak("We're closing up.")
        exit()
        
    else:
        speak("Command is unrecognized.")


def get_random_character():
    url = f'https://rickandmortyapi.com/api/character/?page={randint(1, 42)}'
    response = requests.get(url, timeout=5)
    data = json.loads(response.text)
    character = choice(data['results'])
    return character


while True: 
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get("text", "")
        
        if text:
            print(f"Вы сказали: {text}")
            handle_command(text)
