import os
import sys
import json
import time
from dotenv import load_dotenv

# Import core modules
from core.listen import listen
from core.brain import think
from core.speak import speak

# Import existing skills
from skills.whatsapp import send_whatsapp_message
from skills.system import (
    open_application, close_application, shutdown_system, 
    restart_system, cancel_shutdown, get_current_time, get_current_date
)
from skills.hardware import (
    get_battery_status, adjust_volume, adjust_brightness, 
    get_system_info, set_wallpaper
)
from skills.browser import open_website

# Import NEW Phase 1 skills
from skills.file_manager import (
    create_file, create_folder, delete_item, rename_item, 
    copy_item, search_files, get_file_info, open_location, list_directory
)
from skills.web_search import (
    google_search, wikipedia_query, get_weather, 
    get_news, define_word
)
from skills.reminders import (
    set_reminder, list_reminders, cancel_reminder,
    create_note, read_note, list_notes, delete_note,
    start_reminder_checker
)
from skills.screen_tools import (
    take_screenshot, screenshot_to_clipboard, get_clipboard_text,
    set_clipboard_text, list_screenshots, open_screenshot_folder
)

def execute_action(action):
    """
    Executes a single action based on the tool specified.
    Returns the result message.
    """
    tool = action.get("tool")
    result = ""
    
    try:
        # === EXISTING TOOLS ===
        if tool == "response":
            text = action.get("text", "")
            speak(text)
            result = text
        
        elif tool == "whatsapp_send":
            contact = action.get("contact", "")
            message = action.get("message", "")
            speak(f"Sending message to {contact}")
            send_whatsapp_message(contact, message)
            result = "Message sent"
            speak("Sent")
        
        elif tool == "open_app":
            app_name = action.get("app_name", "")
            speak(f"Opening {app_name}")
            if open_application(app_name):
                result = f"{app_name} opened"
            else:
                result = f"Could not find {app_name}"
                speak(result)
        
        elif tool == "close_app":
            app_name = action.get("app_name", "")
            speak(f"Closing {app_name}")
            if close_application(app_name):
                result = f"{app_name} closed"
            else:
                result = f"Could not close {app_name}"
                speak(result)
        
        elif tool == "open_url":
            url = action.get("url", "")
            speak("Opening browser")
            open_website(url)
            result = f"Opened {url}"
        
        elif tool == "get_battery":
            result = get_battery_status()
            speak(result)
        
        elif tool == "control_volume":
            vol_action = action.get("action", "")
            result = adjust_volume(vol_action)
            speak(result)
        
        elif tool == "adjust_brightness":
            brightness_action = action.get("action", "")
            result = adjust_brightness(brightness_action)
            speak(result)
        
        elif tool == "get_time":
            result = get_current_time()
            speak(result)
        
        elif tool == "get_date":
            result = get_current_date()
            speak(result)
        
        elif tool == "get_system_info":
            result = get_system_info()
            speak(result)
        
        elif tool == "shutdown_system":
            delay = action.get("delay", 0)
            result = shutdown_system(delay)
            speak(result)
        
        elif tool == "restart_system":
            delay = action.get("delay", 0)
            result = restart_system(delay)
            speak(result)
        
        elif tool == "cancel_shutdown":
            result = cancel_shutdown()
            speak(result)
        
        # === FILE MANAGEMENT TOOLS ===
        elif tool == "create_file":
            path = action.get("path", "")
            content = action.get("content", "")
            result = create_file(path, content)
            speak(result)
        
        elif tool == "create_folder":
            path = action.get("path", "")
            result = create_folder(path)
            speak(result)
        
        elif tool == "delete_item":
            path = action.get("path", "")
            result = delete_item(path)
            speak(result)
        
        elif tool == "rename_item":
            old_path = action.get("old_path", "")
            new_path = action.get("new_path", "")
            result = rename_item(old_path, new_path)
            speak(result)
        
        elif tool == "copy_item":
            source = action.get("source", "")
            destination = action.get("destination", "")
            result = copy_item(source, destination)
            speak(result)
        
        elif tool == "search_files":
            query = action.get("query", "")
            location = action.get("location")
            extension = action.get("extension")
            result = search_files(query, location, extension)
            speak(result)
        
        elif tool == "get_file_info":
            path = action.get("path", "")
            result = get_file_info(path)
            speak(result)
        
        elif tool == "open_location":
            path = action.get("path", "")
            result = open_location(path)
            speak(result)
        
        elif tool == "list_directory":
            path = action.get("path", ".")
            result = list_directory(path)
            speak(result)
        
        # === WEB SEARCH TOOLS ===
        elif tool == "google_search":
            query = action.get("query", "")
            num_results = action.get("num_results", 3)
            speak(f"Searching for {query}")
            result = google_search(query, num_results)
            speak(result)
        
        elif tool == "wikipedia":
            topic = action.get("topic", "")
            speak(f"Looking up {topic} on Wikipedia")
            result = wikipedia_query(topic)
            speak(result)
        
        elif tool == "get_weather":
            city = action.get("city", "")
            speak(f"Getting weather for {city}")
            result = get_weather(city)
            speak(result)
        
        elif tool == "get_news":
            category = action.get("category", "general")
            speak(f"Fetching {category} news")
            result = get_news(category)
            speak(result)
        
        elif tool == "define_word":
            word = action.get("word", "")
            speak(f"Looking up definition of {word}")
            result = define_word(word)
            speak(result)
        
        # === REMINDER & NOTES TOOLS ===
        elif tool == "set_reminder":
            message = action.get("message", "")
            time_str = action.get("time", "")
            result = set_reminder(message, time_str)
            speak(result)
        
        elif tool == "list_reminders":
            result = list_reminders()
            speak(result)
        
        elif tool == "cancel_reminder":
            index = action.get("index", 0)
            result = cancel_reminder(index)
            speak(result)
        
        elif tool == "create_note":
            title = action.get("title", "")
            content = action.get("content", "")
            result = create_note(title, content)
            speak(result)
        
        elif tool == "read_note":
            title = action.get("title", "")
            result = read_note(title)
            speak(result)
        
        elif tool == "list_notes":
            result = list_notes()
            speak(result)
        
        elif tool == "delete_note":
            title = action.get("title", "")
            result = delete_note(title)
            speak(result)
        
        # === SCREENSHOT & CLIPBOARD TOOLS ===
        elif tool == "take_screenshot":
            save_path = action.get("save_path")
            result = take_screenshot(save_path=save_path)
            speak(result)
        
        elif tool == "screenshot_to_clipboard":
            result = screenshot_to_clipboard()
            speak(result)
        
        elif tool == "get_clipboard":
            result = get_clipboard_text()
            speak(result)
        
        elif tool == "set_clipboard":
            text = action.get("text", "")
            result = set_clipboard_text(text)
            speak(result)
        
        elif tool == "list_screenshots":
            result = list_screenshots()
            speak(result)
        
        elif tool == "open_screenshot_folder":
            result = open_screenshot_folder()
            speak(result)
        
        else:
            result = f"Unknown tool: {tool}"
            speak("I'm not sure how to do that yet.")
        
    except Exception as e:
        result = f"Error executing {tool}: {str(e)}"
        print(result)
        speak("I encountered an error while doing that.")
    
    return result

def main():
    # Load environment variables
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("CRITICAL ERROR: GROQ_API_KEY is missing.")
        print("Please edit the .env file and add your Groq API Key.")
        speak("I need a brain. Please check your settings.")
        return

    print("=" * 60)
    print("CODE NEXUS - COMPLETE WINDOWS AGENT")
    print("=" * 60)
    print("Features: File Management, Web Search, Reminders, Screenshots, System Control")
    print("=" * 60)
    
    speak("System online. All features loaded. I am listening.")
    
    # Start the reminder checker in background
    start_reminder_checker()

    while True:
        try:
            # 1. Listen for user input
            user_text = listen()
            
            if not user_text:
                continue  # Silence or noise
            
            # Exit commands
            if "exit" in user_text.lower() or "stop listening" in user_text.lower():
                speak("Shutting down. Goodbye.")
                break

            # 2. Think - Get AI decision
            decisions = think(user_text)
            
            # Ensure decisions is a list
            if not isinstance(decisions, list):
                decisions = [decisions]
            
            # 3. Act - Execute all decisions
            for decision in decisions:
                result = execute_action(decision)
                print(f"[Result] {result}")
            
            print("-" * 60)

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            speak("Shutting down.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("I encountered an error.")

if __name__ == "__main__":
    main()
