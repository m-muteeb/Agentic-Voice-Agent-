import os

def install_startup():
    try:
        # 1. Get Startup Folder
        appdata = os.getenv("APPDATA")
        if not appdata:
            print("Error: Could not find APPDATA.")
            return

        startup_dir = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")
        if not os.path.exists(startup_dir):
            print(f"Error: Startup folder not found at {startup_dir}")
            return

        # 2. Define Paths
        # Root of the project (parent of scripts/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        run_bat_path = os.path.join(project_root, "run.bat")

        # 3. Create 'NexusBoot.bat' in Startup
        # Content: CD to project, then run run.bat
        # Using 'start "" ...' to launch it.
        # We use a VBS script trick to run it invisible if we wanted, 
        # but for now let's just make it run.
        
        target_bat = os.path.join(startup_dir, "NexusBoot.bat")
        
        bat_content = f'@echo off\ncd /d "{project_root}"\ncall run.bat'
        
        with open(target_bat, "w") as f:
            f.write(bat_content)
            
        print(f"✅ Created startup file: {target_bat}")
        print("Nexus will launch on next login.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    install_startup()
