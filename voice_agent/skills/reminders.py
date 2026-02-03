import json
import os
from datetime import datetime, timedelta
import threading
import time

# Data directory for reminders and notes
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")
NOTES_DIR = os.path.join(DATA_DIR, "notes")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)

# Global reminders list
ACTIVE_REMINDERS = []
REMINDER_THREAD = None

def load_reminders():
    """Load reminders from file."""
    global ACTIVE_REMINDERS
    try:
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                ACTIVE_REMINDERS = json.load(f)
        else:
            ACTIVE_REMINDERS = []
    except Exception as e:
        print(f"Error loading reminders: {e}")
        ACTIVE_REMINDERS = []

def save_reminders():
    """Save reminders to file."""
    try:
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(ACTIVE_REMINDERS, f, indent=2)
    except Exception as e:
        print(f"Error saving reminders: {e}")

def parse_time_string(time_str):
    """
    Parses time strings like:
    - "in 5 minutes"
    - "in 2 hours"
    - "at 3:00 PM"
    - "at 15:30"
    Returns datetime object or None if parsing fails.
    """
    try:
        time_str = time_str.lower().strip()
        
        # Handle "in X minutes/hours" format
        if "in" in time_str:
            if "minute" in time_str:
                # Extract number
                parts = time_str.split()
                if len(parts) >= 2:
                    minutes = int(parts[1])
                    return datetime.now() + timedelta(minutes=minutes)
            elif "hour" in time_str:
                parts = time_str.split()
                if len(parts) >= 2:
                    hours = int(parts[1])
                    return datetime.now() + timedelta(hours=hours)
        
        # Handle "at HH:MM" format
        elif "at" in time_str:
            time_part = time_str.replace("at", "").strip()
            
            # Try parsing with AM/PM
            for fmt in ["%I:%M %p", "%I %p", "%H:%M"]:
                try:
                    time_obj = datetime.strptime(time_part, fmt).time()
                    target = datetime.combine(datetime.now().date(), time_obj)
                    
                    # If time has passed today, schedule for tomorrow
                    if target < datetime.now():
                        target += timedelta(days=1)
                    
                    return target
                except ValueError:
                    continue
        
        return None
    except Exception as e:
        print(f"Error parsing time: {e}")
        return None

def set_reminder(message, time_str):
    """
    Sets a new reminder.
    time_str: string like "in 5 minutes", "at 3:00 PM", etc.
    Returns confirmation message or error.
    """
    try:
        target_time = parse_time_string(time_str)
        
        if not target_time:
            return f"Could not understand time '{time_str}'. Try 'in 5 minutes' or 'at 3:00 PM'"
        
        reminder = {
            "message": message,
            "time": target_time.isoformat(),
            "created": datetime.now().isoformat()
        }
        
        ACTIVE_REMINDERS.append(reminder)
        save_reminders()
        
        # Start reminder checker if not running
        start_reminder_checker()
        
        time_until = target_time - datetime.now()
        if time_until.total_seconds() < 3600:
            time_desc = f"{int(time_until.total_seconds() / 60)} minutes"
        else:
            time_desc = target_time.strftime("%I:%M %p")
        
        return f"Reminder set for {time_desc}: {message}"
    except Exception as e:
        return f"Error setting reminder: {e}"

def list_reminders():
    """
    Lists all active reminders.
    Returns formatted list or message if none exist.
    """
    try:
        if not ACTIVE_REMINDERS:
            return "You have no active reminders."
        
        result = f"📋 Active Reminders ({len(ACTIVE_REMINDERS)}):\n\n"
        for i, reminder in enumerate(ACTIVE_REMINDERS, 1):
            message = reminder['message']
            time_str = datetime.fromisoformat(reminder['time']).strftime("%I:%M %p on %b %d")
            result += f"{i}. {message} - {time_str}\n"
        
        return result
    except Exception as e:
        return f"Error listing reminders: {e}"

def cancel_reminder(index):
    """
    Cancels a reminder by index (1-based).
    Returns confirmation or error message.
    """
    try:
        if index < 1 or index > len(ACTIVE_REMINDERS):
            return f"Invalid reminder number. You have {len(ACTIVE_REMINDERS)} reminders."
        
        removed = ACTIVE_REMINDERS.pop(index - 1)
        save_reminders()
        
        return f"Reminder cancelled: {removed['message']}"
    except Exception as e:
        return f"Error cancelling reminder: {e}"

def check_reminders():
    """
    Background function that checks for due reminders.
    Runs in a separate thread.
    """
    global ACTIVE_REMINDERS
    
    while True:
        try:
            now = datetime.now()
            due_reminders = []
            
            # Check for due reminders
            for reminder in ACTIVE_REMINDERS[:]:  # Iterate over copy
                reminder_time = datetime.fromisoformat(reminder['time'])
                if reminder_time <= now:
                    due_reminders.append(reminder)
                    ACTIVE_REMINDERS.remove(reminder)
            
            # Trigger due reminders
            for reminder in due_reminders:
                trigger_reminder(reminder['message'])
            
            if due_reminders:
                save_reminders()
            
            # Check every 30 seconds
            time.sleep(30)
        except Exception as e:
            print(f"Error in reminder checker: {e}")
            time.sleep(30)

def trigger_reminder(message):
    """
    Triggers a reminder notification.
    Uses Windows toast notification if available, otherwise prints.
    """
    try:
        # Try Windows 10 toast notification
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                "Reminder",
                message,
                duration=10,
                threaded=True
            )
        except ImportError:
            # Fallback: print and try to speak
            print(f"\n🔔 REMINDER: {message}\n")
            # You could also integrate with speak here
    except Exception as e:
        print(f"Error triggering reminder: {e}")

def start_reminder_checker():
    """Starts the background reminder checker thread if not already running."""
    global REMINDER_THREAD
    
    if REMINDER_THREAD is None or not REMINDER_THREAD.is_alive():
        load_reminders()
        REMINDER_THREAD = threading.Thread(target=check_reminders, daemon=True)
        REMINDER_THREAD.start()

# ===== Notes Functions =====

def create_note(title, content):
    """
    Creates a new note with the given title and content.
    Returns confirmation message or error.
    """
    try:
        # Sanitize title for filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}.txt"
        filepath = os.path.join(NOTES_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
        
        return f"Note '{title}' created successfully."
    except Exception as e:
        return f"Error creating note: {e}"

def read_note(title):
    """
    Reads and returns the content of a note.
    Returns note content or error message.
    """
    try:
        # Find matching note file
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}.txt"
        filepath = os.path.join(NOTES_DIR, filename)
        
        if not os.path.exists(filepath):
            # Try to find partial match
            for file in os.listdir(NOTES_DIR):
                if title.lower() in file.lower():
                    filepath = os.path.join(NOTES_DIR, file)
                    break
            else:
                return f"Note '{title}' not found."
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        return f"Error reading note: {e}"

def list_notes():
    """
    Lists all saved notes.
    Returns formatted list of notes or message if none exist.
    """
    try:
        notes = [f for f in os.listdir(NOTES_DIR) if f.endswith('.txt')]
        
        if not notes:
            return "You have no saved notes."
        
        result = f"📝 Saved Notes ({len(notes)}):\n\n"
        for i, note in enumerate(notes, 1):
            title = note.replace('.txt', '')
            filepath = os.path.join(NOTES_DIR, note)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
            result += f"{i}. {title} (modified: {modified})\n"
        
        return result
    except Exception as e:
        return f"Error listing notes: {e}"

def delete_note(title):
    """
    Deletes a note by title.
    Returns confirmation or error message.
    """
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}.txt"
        filepath = os.path.join(NOTES_DIR, filename)
        
        if not os.path.exists(filepath):
            # Try to find partial match
            for file in os.listdir(NOTES_DIR):
                if title.lower() in file.lower():
                    filepath = os.path.join(NOTES_DIR, file)
                    break
            else:
                return f"Note '{title}' not found."
        
        os.remove(filepath)
        return f"Note '{title}' deleted."
    except Exception as e:
        return f"Error deleting note: {e}"

# Initialize reminders on module import
load_reminders()
