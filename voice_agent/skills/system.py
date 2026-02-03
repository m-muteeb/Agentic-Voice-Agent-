from AppOpener import open, close
import os
import subprocess
from datetime import datetime

def open_special_location(location_name):
    """
    Opens Windows special locations like This PC, Recycle Bin, etc.
    Returns True if successful, False otherwise.
    """
    location_name_lower = location_name.lower()
    
    # Map common names to Windows shell commands
    special_locations = {
        "this pc": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
        "my computer": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
        "computer": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
        "recycle bin": "explorer.exe ::{645FF040-5081-101B-9F08-00AA002F954E}",
        "trash": "explorer.exe ::{645FF040-5081-101B-9F08-00AA002F954E}",
        "downloads": "explorer.exe shell:Downloads",
        "documents": "explorer.exe shell:Personal",
        "my documents": "explorer.exe shell:Personal",
        "pictures": "explorer.exe shell:My Pictures",
        "videos": "explorer.exe shell:My Video",
        "music": "explorer.exe shell:My Music",
        "desktop": "explorer.exe shell:Desktop",
        "network": "explorer.exe ::{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
        "control panel": "control",
        "settings": "ms-settings:",
    }
    
    # Check if it's a special location
    for key, command in special_locations.items():
        if key in location_name_lower:
            try:
                print(f"Opening {location_name}...")
                subprocess.Popen(command, shell=True)
                return True
            except Exception as e:
                print(f"Error opening {location_name}: {e}")
                return False
    
    return False

def open_application(app_name):
    """Opens a Windows application or special location."""
    print(f"Opening {app_name}...")
    
    # First try special locations
    if open_special_location(app_name):
        return True
    
    # Then try regular applications
    try:
        open(app_name, match_closest=True, output=False)
        return True
    except Exception as e:
        print(f"Failed to open {app_name}: {e}")
        return False

def close_application(app_name):
    """Closes a Windows application using taskkill for robustness."""
    print(f"Closing {app_name}...")
    try:
        # First try robust taskkill
        # /f = force, /im = image name (we try to guess executable name)
        # This is a heuristic. AppOpener's close is sometimes weak.
        
        # 1. Try AppOpener first
        close(app_name, match_closest=True, output=False)
        
        # 2. Force kill common names just in case
        exe_name = app_name.lower().replace(" ", "") + ".exe"
        os.system(f"taskkill /f /im {exe_name} >nul 2>&1")
        
        # 3. Handle Chrome Specifically
        if "chrome" in app_name.lower():
             os.system("taskkill /f /im chrome.exe >nul 2>&1")
             
        return True
    except Exception as e:
        print(f"Error closing {app_name}: {e}")
        return False

def shutdown_system(delay=0):
    """
    Shutdown the computer.
    delay: delay in seconds before shutdown (default 0)
    """
    try:
        os.system(f"shutdown /s /t {delay}")
        if delay > 0:
            return f"System will shutdown in {delay} seconds."
        else:
            return "Shutting down now."
    except Exception as e:
        return f"Error shutting down: {e}"

def restart_system(delay=0):
    """
    Restart the computer.
    delay: delay in seconds before restart (default 0)
    """
    try:
        os.system(f"shutdown /r /t {delay}")
        if delay > 0:
            return f"System will restart in {delay} seconds."
        else:
            return "Restarting now."
    except Exception as e:
        return f"Error restarting: {e}"

def cancel_shutdown():
    """Cancel a pending shutdown or restart."""
    try:
        os.system("shutdown /a")
        return "Shutdown or restart cancelled."
    except Exception as e:
        return f"Error cancelling: {e}"

def get_current_time():
    """Returns the current time in a readable format."""
    now = datetime.now()
    return now.strftime("It is %I:%M %p")

def get_current_date():
    """Returns the current date in a readable format."""
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y")
