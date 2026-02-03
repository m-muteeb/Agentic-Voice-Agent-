import pyautogui
import time
from AppOpener import open
import os

def send_whatsapp_message(contact_name, message):
    """
    Sends a WhatsApp message using desktop automation.
    Prerequisite: WhatsApp Desktop App installed and logged in.
    """
    print(f"Executing: Send '{message}' to {contact_name}")
    
    # 1. Open WhatsApp
    # Using AppOpener or os.system
    # open("whatsapp") often works, but let's try a safer way via run command if needed.
    # AppOpener is robust for windows store apps.
    try:
        open("whatsapp", match_closest=True)
    except:
        # Fallback
        os.system("start whatsapp:")
    
    # Wait for app to open
    time.sleep(3) # Adjust based on PC speed
    
    # 2. Search for contact
    # Ctrl + F usually focuses search in WhatsApp Desktop
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # Type contact name
    pyautogui.write(contact_name)
    time.sleep(1.0) # Wait for search results
    
    # Select first result (Down arrow + Enter, or just Enter if unique)
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 3. Type message
    pyautogui.write(message)
    time.sleep(0.5)
    
    # 4. Send
    pyautogui.press('enter')
    print("Message sent.")

if __name__ == "__main__":
    # Test
    send_whatsapp_message("Ali", "This is a test from Python")
