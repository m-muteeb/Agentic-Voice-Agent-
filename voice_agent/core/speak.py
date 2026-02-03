import asyncio
import edge_tts
import os
import pygame

# Configuration
VOICE = "en-US-AriaNeural"  # or en-GB-SoniaNeural, en-US-ChristopherNeural
OUTPUT_FILE = "response.mp3"

async def generate_audio(text):
    """Generates MP3 audio from text using Edge-TTS."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def play_audio():
    """Plays the generated audio file using pygame to avoid blocking issues."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        # Clean up
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    except Exception as e:
        print(f"Error playing audio: {e}")

def speak(text):
    """Synchronous wrapper for the speech function."""
    try:
        print(f"Assistant: {text}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_audio(text))
        play_audio()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

if __name__ == "__main__":
    speak("Hello! I am your AI assistant. How can I help you?")
