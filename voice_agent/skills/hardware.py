import psutil
import pyautogui
import ctypes
import os

def get_battery_status():
    """Returns a string describing battery status with time remaining."""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "Battery information not available."
        
        percent = battery.percent
        charging = battery.power_plugged
        
        # Build status message
        if charging:
            status = f"Battery is at {percent}% and charging."
        else:
            status = f"Battery is at {percent}%."
            # Add time remaining if available
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                if hours > 0:
                    status += f" Approximately {hours} hours and {minutes} minutes remaining."
                else:
                    status += f" Approximately {minutes} minutes remaining."
        
        return status
    except Exception as e:
        return f"Could not read battery: {e}"

def adjust_volume(action):
    """
    Adjusts system volume.
    action: 'up', 'down', 'mute'
    """
    try:
        if action == "up":
            # Press Volume Up multiple times for noticeable change
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increased."
        elif action == "down":
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume decreased."
        elif action == "mute":
            pyautogui.press("volumemute")
            return "Volume toggled mute."
        return "Unknown volume command."
    except Exception as e:
        return f"Error adjusting volume: {e}"

def adjust_brightness(action):
    """
    Adjusts screen brightness.
    action: 'up', 'down', or an integer percentage (0-100)
    """
    try:
        import wmi
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        
        # Get current brightness
        brightness_info = c.WmiMonitorBrightness()[0]
        current = brightness_info.CurrentBrightness
        
        if action == "up":
            new_brightness = min(current + 10, 100)
            methods.WmiSetBrightness(new_brightness, 0)
            return f"Brightness increased to {new_brightness}%."
        elif action == "down":
            new_brightness = max(current - 10, 0)
            methods.WmiSetBrightness(new_brightness, 0)
            return f"Brightness decreased to {new_brightness}%."
        elif isinstance(action, int) and 0 <= action <= 100:
            methods.WmiSetBrightness(action, 0)
            return f"Brightness set to {action}%."
        else:
            return "Unknown brightness command. Use 'up', 'down', or a number 0-100."
    except ImportError:
        return "WMI module not installed. Run: pip install WMI"
    except Exception as e:
        return f"Could not adjust brightness: {e}"

def get_system_info():
    """Returns CPU and RAM usage information."""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)
        
        return f"CPU usage is at {cpu_percent}%. RAM usage is {ram_percent}%, using {ram_used_gb:.1f} GB of {ram_total_gb:.1f} GB."
    except Exception as e:
        return f"Could not get system info: {e}"

def set_wallpaper(path=None):
    """
    Sets the desktop wallpaper.
    If path is None, it tries to find a default image or does nothing.
    """
    try:
        if not path:
             # Just a placeholder if no path provided. 
             # In a real scenario, we might have a 'wallpapers' folder.
             return "Please provide a path to an image."
        
        if not os.path.exists(path):
            return f"Image not found at {path}"

        # Windows API call
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
        return "Wallpaper updated."
    except Exception as e:
        return f"Error setting wallpaper: {e}"
