import speech_recognition as sr
import os
import tempfile

def listen():
    """
    Listens to the microphone and returns the transcribed text.
    Uses Google Speech Recognition (Online, Free, Fast).
    MAXIMUM SENSITIVITY - Catches even quiet/soft speech.
    """
    recognizer = sr.Recognizer()
    
    # ULTRA-SENSITIVE SETTINGS - Will catch even whispers
    recognizer.energy_threshold = 50  # Extremely low - maximum sensitivity
    recognizer.dynamic_energy_threshold = True  # Re-enable for continuous adaptation
    recognizer.dynamic_energy_adjustment_damping = 0.10  # Very aggressive adjustment
    recognizer.dynamic_energy_ratio = 1.2  # Low ratio for sensitive detection
    recognizer.pause_threshold = 1.0  # Wait a full second for complete sentences
    
    with sr.Microphone() as source:
        print("🎤 Listening...")
        
        # Comprehensive ambient noise adjustment
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1.2)
            print(f"  [Threshold: {recognizer.energy_threshold}]")
        except:
            pass
        
        try:
            # Maximum timeout and phrase limit
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            print("⏳ Processing...")
            
            # Use Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"✅ HEARD: {text}")
            
            # NO WAKE WORD - continuous listening
            return text

        except sr.WaitTimeoutError:
            print("⏱️ Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return None

if __name__ == "__main__":
    while True:
        text = listen()
        if text:
            if "exit" in text.lower():
                break
