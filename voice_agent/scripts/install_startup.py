import os
import sys
import winshell
from win32com.client import Dispatch

def create_shortcut():
    """
    Creates a shortcut to run.bat in the Windows Startup folder.
    Requires: pip install pywin32 winshell
    """
    try:
        # Paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get to voice_agent root from scripts/
        root_dir = os.path.dirname(current_dir)
        target = os.path.join(root_dir, "run.bat")
        
        # Verify target exists
        if not os.path.exists(target):
            print(f"Error: Could not find run.bat at {target}")
            return

        # Startup Folder
        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, "NexusAssistant.lnk")
        
        print(f"Target: {target}")
        print(f"Startup: {shortcut_path}")
        
        # Create Shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = root_dir
        shortcut.IconLocation = target 
        shortcut.save()
        
        print("✅ Successfully installed to Startup!")
        print("Nexus will now launch automatically when you log in.")
        
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")
        print("Try running as Administrator or installing 'pywin32' and 'winshell'.")

if __name__ == "__main__":
    create_shortcut()
