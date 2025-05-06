# alert_voice.py
import pyttsx3

# Voice Engine Initialize karo
def init_voice():
    engine = pyttsx3.init()  # pyttsx3 engine ko initialize karo
    return engine

# Alert dene ka function
def speak_alert(engine, text="Person detected. Please stay out of this area."):
    print("[Voice Alert] 🎙️", text)
    engine.say(text)  # Alert awaaz me bolega
    engine.runAndWait()  # Wait until voice finishes
