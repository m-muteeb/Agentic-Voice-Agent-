import pyautogui
import pyperclip
from PIL import ImageGrab
from datetime import datetime
import os

# Default screenshot directory
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(region=None, save_path=None):
    """
    Takes a screenshot of the entire screen or a specific region.
    
    Args:
        region: Optional tuple (x, y, width, height) for specific region
        save_path: Optional path to save screenshot. If None, auto-generates filename
    
    Returns:
        Success message with filepath or error message
    """
    try:
        if region:
            # Capture specific region
            screenshot = pyautogui.screenshot(region=region)
        else:
            # Capture entire screen
            screenshot = pyautogui.screenshot()
        
        # Generate filename if not provided
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            save_path = os.path.join(SCREENSHOT_DIR, filename)
        
        # Save screenshot
        screenshot.save(save_path)
        
        return f"Screenshot saved to {save_path}"
    except Exception as e:
        return f"Error taking screenshot: {e}"

def screenshot_to_clipboard():
    """
    Takes a screenshot and copies it to clipboard.
    Returns success message or error.
    """
    try:
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Convert to clipboard format and copy
        # Note: This requires PIL/Pillow
        import io
        output = io.BytesIO()
        screenshot.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Remove BMP header
        output.close()
        
        # Copy to clipboard using win32clipboard
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return "Screenshot copied to clipboard."
        except ImportError:
            # Fallback: save to file and notify
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            save_path = os.path.join(SCREENSHOT_DIR, filename)
            screenshot.save(save_path)
            return f"Screenshot saved to {save_path} (clipboard copy requires pywin32)"
    except Exception as e:
        return f"Error taking screenshot to clipboard: {e}"

def take_region_screenshot(x, y, width, height, save_path=None):
    """
    Takes a screenshot of a specific region.
    
    Args:
        x, y: Top-left corner coordinates
        width, height: Size of region
        save_path: Optional save path
    
    Returns:
        Success message or error
    """
    return take_screenshot(region=(x, y, width, height), save_path=save_path)

def get_clipboard_text():
    """
    Reads text from the clipboard.
    Returns clipboard text or error message.
    """
    try:
        text = pyperclip.paste()
        if text:
            return f"Clipboard content: {text}"
        else:
            return "Clipboard is empty or contains non-text data."
    except Exception as e:
        return f"Error reading clipboard: {e}"

def set_clipboard_text(text):
    """
    Sets the clipboard to the specified text.
    Returns confirmation or error message.
    """
    try:
        pyperclip.copy(text)
        return f"Text copied to clipboard."
    except Exception as e:
        return f"Error setting clipboard: {e}"

def clear_clipboard():
    """
    Clears the clipboard.
    Returns confirmation message.
    """
    try:
        pyperclip.copy('')
        return "Clipboard cleared."
    except Exception as e:
        return f"Error clearing clipboard: {e}"

def capture_window_screenshot(window_title):
    """
    Captures a screenshot of a specific window.
    Note: This is a simplified version. Full implementation would require pywin32.
    
    Args:
        window_title: Title of the window to capture
    
    Returns:
        Success message or error
    """
    try:
        # This is a basic implementation
        # For production, you'd want to use pywin32 to get window bounds
        import pygetwindow as gw
        
        try:
            # Find window
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                return f"Window '{window_title}' not found."
            
            window = windows[0]
            
            # Get window region
            region = (window.left, window.top, window.width, window.height)
            
            # Take screenshot of that region
            return take_screenshot(region=region)
        except ImportError:
            return "Window-specific screenshots require pygetwindow. Taking full screenshot instead."
    except Exception as e:
        return f"Error capturing window screenshot: {e}"

def list_screenshots():
    """
    Lists all saved screenshots.
    Returns formatted list of screenshots.
    """
    try:
        screenshots = [f for f in os.listdir(SCREENSHOT_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not screenshots:
            return "No screenshots found."
        
        # Sort by modification time (newest first)
        screenshots.sort(key=lambda x: os.path.getmtime(os.path.join(SCREENSHOT_DIR, x)), reverse=True)
        
        result = f"📸 Screenshots ({len(screenshots)}):\n\n"
        for i, screenshot in enumerate(screenshots[:10], 1):  # Show last 10
            filepath = os.path.join(SCREENSHOT_DIR, screenshot)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            result += f"{i}. {screenshot} - {modified}\n"
        
        if len(screenshots) > 10:
            result += f"\n... and {len(screenshots) - 10} more."
        
        return result
    except Exception as e:
        return f"Error listing screenshots: {e}"

def open_screenshot_folder():
    """
    Opens the screenshot folder in Windows Explorer.
    Returns confirmation message.
    """
    try:
        os.startfile(SCREENSHOT_DIR)
        return f"Opened screenshot folder: {SCREENSHOT_DIR}"
    except Exception as e:
        return f"Error opening screenshot folder: {e}"
