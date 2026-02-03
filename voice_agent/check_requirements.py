import importlib.util
import sys

dependencies = [
    "speech_recognition",
    "whisper",
    "edge_tts",
    "pygame",
    "groq",
    "pyautogui",
    "AppOpener",
    "dotenv",
    "sounddevice",
    "psutil",
    "requests",
    "bs4",  # beautifulsoup4
    "PIL",  # Pillow
    "pyperclip",
    "win10toast",
    "schedule"
]

missing = []

print("Checking dependencies...")
for dep in dependencies:
    # Handle package name vs import name differences
    import_name = dep
    if dep == "speech_recognition": import_name = "speech_recognition"
    if dep == "dotenv": import_name = "dotenv" # actually python-dotenv installs dotenv
    
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(f"[X] Missing: {dep}")
        missing.append(dep)
    else:
        print(f"[OK] Found: {dep}")

if missing:
    print("\nSome dependencies are missing. Installing them now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Installation attempt complete. Please verify.")
else:
    print("\nAll systems go! You are ready to configure the .env file.")
