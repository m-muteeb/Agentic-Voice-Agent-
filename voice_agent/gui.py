import customtkinter as ctk
import threading
import time
import os
import math
from datetime import datetime
from dotenv import load_dotenv
import psutil

# Import core modules
from core.listen import listen
from core.brain import think
from core.speak import speak

# Import all skills - existing
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
try:
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
    PHASE1_LOADED = True
except ImportError as e:
    print(f"Warning: Some Phase 1 features not available: {e}")
    PHASE1_LOADED = False

# UI Configuration - Light Theme with Golden & Dark Green
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class EnhancedNexusUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("CODE NEXUS - COMPLETE WINDOWS AGENT")
        self.geometry("1400x850")
        self.resizable(True, True)
        
        # Light elegant background
        self.configure(fg_color="#f5f5f0")
        
        # Load Env
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")

        # Layout Grid
        self.grid_columnconfigure(0, weight=0, minsize=240)  # Sidebar
        self.grid_columnconfigure(1, weight=1)               # Main content
        self.grid_rowconfigure(1, weight=1)

        # --- SIDEBAR ---
        self.create_sidebar()

        # --- MAIN CONTENT ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, rowspan=5, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self.main_frame, 
                                        fg_color=["#1a4d2e", "#144d2e"], 
                                        corner_radius=15, 
                                        height=80, 
                                        border_width=3, 
                                        border_color="#d4af37")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Header layout
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        header_title = ctk.CTkLabel(self.header_frame, 
                                   text="CODE NEXUS",
                                   font=("Georgia", 32, "bold"), 
                                   text_color="#d4af37")
        header_title.grid(row=0, column=0, pady=5, padx=20, sticky="w")
        
        subtitle = ctk.CTkLabel(self.header_frame, 
                              text="Complete Windows Agent - 40+ Tools",
                              font=("Georgia", 12, "italic"), 
                              text_color="#e8d7a8")
        subtitle.grid(row=1, column=0, padx=20, sticky="w")
        
        # Feature counter
        feature_count = "41" if PHASE1_LOADED else "14"
        self.feature_badge = ctk.CTkLabel(self.header_frame,
                                        text=f"{feature_count} TOOLS",
                                        font=("Georgia", 16, "bold"),
                                        text_color="#1a4d2e",
                                        fg_color="#d4af37",
                                        corner_radius=8,
                                        width=100,
                                        height=35)
        self.feature_badge.grid(row=0, column=1, rowspan=2, padx=20, pady=10)

        # --- STATUS BAR (NEW) ---
        self.status_bar_frame = ctk.CTkFrame(self.main_frame,
                                            fg_color="#ffffff",
                                            corner_radius=12,
                                            border_width=2,
                                            border_color="#d4af37",
                                            height=60)
        self.status_bar_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.status_bar_frame.grid_columnconfigure(0, weight=1)
        self.status_bar_frame.grid_columnconfigure(1, weight=1)
        self.status_bar_frame.grid_columnconfigure(2, weight=1)
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(self.status_bar_frame,
                                           text="STATUS: READY",
                                           font=("Georgia", 14, "bold"),
                                           text_color="#1a4d2e")
        self.status_indicator.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        # Processing indicator
        self.processing_indicator = ctk.CTkLabel(self.status_bar_frame,
                                                text="IDLE",
                                                font=("Consolas", 12, "bold"),
                                                text_color="#666666")
        self.processing_indicator.grid(row=0, column=1, pady=10)
        
        # Threshold/Audio level indicator
        self.threshold_label = ctk.CTkLabel(self.status_bar_frame,
                                           text="AUDIO: --",
                                           font=("Consolas", 11),
                                           text_color="#2d7a4f")
        self.threshold_label.grid(row=0, column=2, padx=15, pady=10, sticky="e")

        # --- ACTIVITY LOG ---
        self.log_frame = ctk.CTkFrame(self.main_frame, 
                                     fg_color="#ffffff", 
                                     corner_radius=15, 
                                     border_width=3, 
                                     border_color="#d4af37")
        self.log_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.log_frame.grid_rowconfigure(1, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent", height=40)
        log_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))
        log_header.grid_columnconfigure(0, weight=1)
        
        self.log_title = ctk.CTkLabel(log_header, 
                                     text="ACTIVITY LOG",
                                     font=("Georgia", 16, "bold"), 
                                     text_color="#1a4d2e")
        self.log_title.grid(row=0, column=0, sticky="w")
        
        # Clear log button
        self.clear_btn = ctk.CTkButton(log_header,
                                      text="CLEAR",
                                      command=self.clear_log,
                                      font=("Georgia", 10, "bold"),
                                      fg_color="#8b4513",
                                      hover_color="#6b3410",
                                      text_color="#ffffff",
                                      corner_radius=8,
                                      width=70,
                                      height=25)
        self.clear_btn.grid(row=0, column=1, padx=5, sticky="e")
        
        self.chat_display = ctk.CTkTextbox(self.log_frame, 
                                          state="disabled", 
                                          fg_color="#fefefe", 
                                          font=("Consolas", 10),
                                          text_color="#2c3e50",
                                          wrap="word")
        self.chat_display.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # Configure text tags for colored messages
        self.chat_display.tag_config("user", foreground="#1a4d2e")
        self.chat_display.tag_config("ai", foreground="#2d7a4f")
        self.chat_display.tag_config("system", foreground="#d4af37")
        self.chat_display.tag_config("action", foreground="#8b6914")
        self.chat_display.tag_config("error", foreground="#8b4513")
        self.chat_display.tag_config("status", foreground="#666666")

        # --- CONTROLS ---
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, pady=15)
        
        self.start_btn = ctk.CTkButton(self.btn_frame, 
                                     text="START ASSISTANT", 
                                     command=self.start_listening_thread, 
                                     font=("Georgia", 15, "bold"), 
                                     fg_color="#2d7a4f", 
                                     hover_color="#1a4d2e",
                                     text_color="#ffffff",
                                     corner_radius=25,
                                     height=50,
                                     width=220,
                                     border_width=2,
                                     border_color="#d4af37")
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(self.btn_frame, 
                                    text="STOP", 
                                    command=self.stop_listening, 
                                    font=("Georgia", 15, "bold"), 
                                    fg_color="#8b4513", 
                                    hover_color="#6b3410",
                                    text_color="#ffffff",
                                    corner_radius=25,
                                    height=50,
                                    width=220,
                                    border_width=2,
                                    border_color="#d4af37",
                                    state="disabled")
        self.stop_btn.pack(side="left", padx=10)

        # State
        self.running = False
        self.thread = None
        self.current_audio_level = 0
        
        # Start updates
        self.update_sidebar_stats()
        self.update_status_bar()

    def create_sidebar(self):
        """Create the system stats sidebar"""
        self.sidebar = ctk.CTkFrame(self, 
                                   fg_color="#1a4d2e", 
                                   corner_radius=0, 
                                   border_width=0)
        self.sidebar.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=0, pady=0)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(self.sidebar, 
                                    text="SYSTEM STATS", 
                                    font=("Georgia", 18, "bold"), 
                                    text_color="#d4af37")
        sidebar_title.pack(pady=20)
        
        # Time Card
        self.time_card = self.create_stat_card(self.sidebar, "TIME")
        self.time_value = ctk.CTkLabel(self.time_card, 
                                      text="--:--", 
                                      font=("Georgia", 22, "bold"), 
                                      text_color="#d4af37")
        self.time_value.pack(pady=5)
        
        # Date Card
        self.date_card = self.create_stat_card(self.sidebar, "DATE")
        self.date_value = ctk.CTkLabel(self.date_card, 
                                      text="Loading...", 
                                      font=("Georgia", 10), 
                                      text_color="#e8d7a8",
                                      wraplength=200)
        self.date_value.pack(pady=5)
        
        # Battery Card
        self.battery_card = self.create_stat_card(self.sidebar, "BATTERY")
        self.battery_value = ctk.CTkLabel(self.battery_card, 
                                         text="---%", 
                                         font=("Georgia", 20, "bold"), 
                                         text_color="#2d7a4f")
        self.battery_value.pack(pady=5)
        self.battery_status = ctk.CTkLabel(self.battery_card, 
                                          text="", 
                                          font=("Georgia", 9), 
                                          text_color="#c9b887")
        self.battery_status.pack()
        
        # CPU Card
        self.cpu_card = self.create_stat_card(self.sidebar, "CPU")
        self.cpu_value = ctk.CTkLabel(self.cpu_card, 
                                     text="--%", 
                                     font=("Georgia", 20, "bold"), 
                                     text_color="#d4af37")
        self.cpu_value.pack(pady=5)
        
        # RAM Card
        self.ram_card = self.create_stat_card(self.sidebar, "RAM")
        self.ram_value = ctk.CTkLabel(self.ram_card, 
                                     text="--%", 
                                     font=("Georgia", 20, "bold"), 
                                     text_color="#c9a961")
        self.ram_value.pack(pady=5)
        
        # Features Enabled Card
        self.features_card = self.create_stat_card(self.sidebar, "FEATURES")
        features_text = "Phase 1 Active" if PHASE1_LOADED else "Base Only"
        self.features_value = ctk.CTkLabel(self.features_card,
                                          text=features_text,
                                          font=("Georgia", 11, "bold"),
                                          text_color="#2d7a4f" if PHASE1_LOADED else "#c9a961")
        self.features_value.pack(pady=5)

    def create_stat_card(self, parent, title):
        """Create an elegant stat card"""
        card = ctk.CTkFrame(parent, 
                          fg_color="#2d5a3d", 
                          corner_radius=12, 
                          border_width=2, 
                          border_color="#d4af37")
        card.pack(pady=10, padx=15, fill="x")
        
        label = ctk.CTkLabel(card, 
                           text=title, 
                           font=("Georgia", 12, "bold"), 
                           text_color="#c9b887")
        label.pack(pady=(10, 0))
        
        return card

    def update_sidebar_stats(self):
        """Update sidebar statistics"""
        try:
            # Time
            now = datetime.now()
            self.time_value.configure(text=now.strftime("%I:%M %p"))
            self.date_value.configure(text=now.strftime("%A, %B %d"))
            
            # Battery
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                charging = battery.power_plugged
                self.battery_value.configure(text=f"{percent}%")
                status_text = "Charging" if charging else "On Battery"
                self.battery_status.configure(text=status_text)
                
                # Color coding
                if percent > 60:
                    self.battery_value.configure(text_color="#2d7a4f")
                elif percent > 20:
                    self.battery_value.configure(text_color="#d4af37")
                else:
                    self.battery_value.configure(text_color="#8b4513")
            
            # CPU
            cpu = psutil.cpu_percent(interval=0.1)
            self.cpu_value.configure(text=f"{cpu}%")
            
            # RAM
            ram = psutil.virtual_memory()
            self.ram_value.configure(text=f"{ram.percent}%")
            
        except Exception as e:
            print(f"Error updating stats: {e}")
        
        # Update every 2 seconds
        self.after(2000, self.update_sidebar_stats)

    def update_status_bar(self):
        """Update the status bar with current processing state"""
        try:
            # Update audio level if available
            if hasattr(self, 'current_audio_level') and self.running:
                level_text = f"AUDIO: {self.current_audio_level:.0f}dB"
                self.threshold_label.configure(text=level_text)
        except:
            pass
        
        self.after(100, self.update_status_bar)

    def clear_log(self):
        """Clear the activity log"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")

    def log(self, sender, message, tag="system"):
        """Add message to activity log with elegant formatting"""
        self.chat_display.configure(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}] {sender}: "
        
        self.chat_display.insert("end", prefix, tag)
        self.chat_display.insert("end", message + "\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def set_status(self, status_text, processing_text="IDLE", audio_level=0):
        """Update all status indicators"""
        self.status_indicator.configure(text=f"STATUS: {status_text}")
        self.processing_indicator.configure(text=processing_text)
        self.current_audio_level = audio_level
        
        # Color coding for processing state
        colors = {
            "IDLE": "#666666",
            "LISTENING": "#2d7a4f",
            "PROCESSING": "#d4af37",
            "THINKING": "#d4af37",
            "RESPONDING": "#3a9861",
            "EXECUTING": "#8b6914"
        }
        self.processing_indicator.configure(text_color=colors.get(processing_text, "#666666"))

    def start_listening_thread(self):
        """Start the agent in a background thread"""
        if self.running:
            return
        
        if not self.api_key:
            self.log("SYSTEM", "CRITICAL: API KEY MISSING", "error")
            return
        
        # Start reminder checker if Phase 1 loaded
        if PHASE1_LOADED:
            try:
                start_reminder_checker()
            except:
                pass
            
        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.thread = threading.Thread(target=self.run_agent, daemon=True)
        self.thread.start()

    def stop_listening(self):
        """Stop the agent"""
        self.running = False
        self.set_status("SHUTTING DOWN", "IDLE")

    def execute_action(self, action):
        """Execute a single action - handles all 40+ tools"""
        tool = action.get("tool")
        
        try:
            # === COMMUNICATION ===
            if tool == "response":
                text = action.get("text", "")
                self.log("NEXUS", text, "ai")
                speak(text)
            
            elif tool == "whatsapp_send":
                contact = action.get("contact", "")
                message = action.get("message", "")
                self.log("ACTION", f"WhatsApp -> {contact}", "action")
                speak(f"Sending message to {contact}")
                send_whatsapp_message(contact, message)
            
            # === APPLICATIONS & WEB ===
            elif tool == "open_app":
                app_name = action.get("app_name", "")
                self.log("ACTION", f"Opening {app_name}", "action")
                speak(f"Opening {app_name}")
                open_application(app_name)
            
            elif tool == "close_app":
                app_name = action.get("app_name", "")
                self.log("ACTION", f"Closing {app_name}", "action")
                speak(f"Closing {app_name}")
                close_application(app_name)
            
            elif tool == "open_url":
                url = action.get("url", "")
                self.log("ACTION", f"Opening {url}", "action")
                speak("Opening website")
                open_website(url)
            
            # === SYSTEM HARDWARE ===
            elif tool == "get_battery":
                result = get_battery_status()
                self.log("NEXUS", result, "ai")
                speak(result)
            
            elif tool == "control_volume":
                vol_action = action.get("action", "")
                result = adjust_volume(vol_action)
                self.log("ACTION", result, "action")
                speak(result)
            
            elif tool == "adjust_brightness":
                bright_action = action.get("action", "")
                result = adjust_brightness(bright_action)
                self.log("ACTION", result, "action")
                speak(result)
            
            elif tool == "get_time":
                result = get_current_time()
                self.log("NEXUS", result, "ai")
                speak(result)
            
            elif tool == "get_date":
                result = get_current_date()
                self.log("NEXUS", result, "ai")
                speak(result)
            
            elif tool == "get_system_info":
                result = get_system_info()
                self.log("NEXUS", result, "ai")
                speak(result)
            
            elif tool == "shutdown_system":
                delay = action.get("delay", 30)
                result = shutdown_system(delay)
                self.log("ACTION", f"Shutdown in {delay}s", "action")
                speak(result)
            
            elif tool == "restart_system":
                delay = action.get("delay", 30)
                result = restart_system(delay)
                self.log("ACTION", f"Restart in {delay}s", "action")
                speak(result)
            
            elif tool == "cancel_shutdown":
                result = cancel_shutdown()
                self.log("ACTION", result, "action")
                speak(result)
            
            # === FILE MANAGEMENT (Phase 1) ===
            elif PHASE1_LOADED and tool == "create_file":
                path = action.get("path", "")
                content = action.get("content", "")
                result = create_file(path, content)
                self.log("FILE", result, "action")
                # Brief confirmation
                speak("Done")
            
            elif PHASE1_LOADED and tool == "create_folder":
                path = action.get("path", "")
                result = create_folder(path)
                self.log("FILE", result, "action")
                # Brief confirmation
                speak("Done")
            
            elif PHASE1_LOADED and tool == "delete_item":
                path = action.get("path", "")
                result = delete_item(path)
                self.log("FILE", result, "action")
                speak(result)
            
            elif PHASE1_LOADED and tool == "search_files":
                query = action.get("query", "")
                location = action.get("location")
                extension = action.get("extension")
                self.set_status("READY", "EXECUTING")
                result = search_files(query, location, extension)
                self.log("FILE", result, "action")
                speak(f"Search complete. Check log for results.")
            
            elif PHASE1_LOADED and tool == "get_file_info":
                path = action.get("path", "")
                result = get_file_info(path)
                self.log("FILE", result, "action")
                speak(result)
            
            elif PHASE1_LOADED and tool == "open_location":
                path = action.get("path", "")
                result = open_location(path)
                self.log("FILE", result, "action")
                speak(result)
            
            # === WEB SEARCH (Phase 1) ===
            elif PHASE1_LOADED and tool == "google_search":
                query = action.get("query", "")
                self.set_status("READY", "EXECUTING")
                self.log("WEB", f"Searching: {query}", "action")
                speak(f"Searching for {query}")
                result = google_search(query)
                self.log("WEB", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "wikipedia":
                topic = action.get("topic", "")
                self.set_status("READY", "EXECUTING")
                self.log("WEB", f"Wikipedia: {topic}", "action")
                speak(f"Looking up {topic}")
                result = wikipedia_query(topic)
                self.log("WEB", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "get_weather":
                city = action.get("city", "")
                self.set_status("READY", "EXECUTING")
                self.log("WEB", f"Weather: {city}", "action")
                speak(f"Getting weather for {city}")
                result = get_weather(city)
                self.log("WEB", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "get_news":
                category = action.get("category", "general")
                self.set_status("READY", "EXECUTING")
                self.log("WEB", f"News: {category}", "action")
                speak(f"Fetching {category} news")
                result = get_news(category)
                self.log("WEB", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "define_word":
                word = action.get("word", "")
                self.set_status("READY", "EXECUTING")
                self.log("WEB", f"Define: {word}", "action")
                result = define_word(word)
                self.log("WEB", result, "ai")
                speak(result)
            
            # === REMINDERS & NOTES (Phase 1) ===
            elif PHASE1_LOADED and tool == "set_reminder":
                message = action.get("message", "")
                time_str = action.get("time", "")
                result = set_reminder(message, time_str)
                self.log("REMINDER", result, "action")
                speak(result)
            
            elif PHASE1_LOADED and tool == "list_reminders":
                result = list_reminders()
                self.log("REMINDER", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "create_note":
                title = action.get("title", "")
                content = action.get("content", "")
                result = create_note(title, content)
                self.log("NOTE", result, "action")
                speak(result)
            
            elif PHASE1_LOADED and tool == "read_note":
                title = action.get("title", "")
                result = read_note(title)
                self.log("NOTE", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "list_notes":
                result = list_notes()
                self.log("NOTE", result, "ai")
                speak(result)
            
            # === SCREENSHOTS & CLIPBOARD (Phase 1) ===
            elif PHASE1_LOADED and tool == "take_screenshot":
                save_path = action.get("save_path")
                result = take_screenshot(save_path=save_path)
                self.log("SCREEN", result, "action")
                # Brief confirmation
                speak("Taken")
            
            elif PHASE1_LOADED and tool == "screenshot_to_clipboard":
                result = screenshot_to_clipboard()
                self.log("SCREEN", result, "action")
                speak(result)
            
            elif PHASE1_LOADED and tool == "get_clipboard":
                result = get_clipboard_text()
                self.log("CLIPBOARD", result, "ai")
                speak(result)
            
            elif PHASE1_LOADED and tool == "set_clipboard":
                text = action.get("text", "")
                result = set_clipboard_text(text)
                self.log("CLIPBOARD", result, "action")
                speak(result)
            
            else:
                self.log("ERROR", f"Unknown tool: {tool}", "error")
                speak("I'm not sure how to do that yet")
        
        except Exception as e:
            error_msg = f"Error executing {tool}: {str(e)}"
            self.log("ERROR", error_msg, "error")
            speak("I encountered an error while doing that")

    def run_agent(self):
        """Main agent loop - continuous listening"""
        self.set_status("ACTIVE", "IDLE")
        
        greeting = "Code Nexus is ready. I'm listening."
        self.log("NEXUS", greeting, "ai")
        speak(greeting)
        
        while self.running:
            try:
                # Listening phase
                self.set_status("ACTIVE", "LISTENING")
                self.log("STATUS", "Listening for command...", "status")
                user_text = listen()
                
                if not self.running:
                    break
                
                if not user_text:
                    time.sleep(0.2)
                    continue

                self.log("USER", user_text, "user")

                # Thinking phase
                self.set_status("ACTIVE", "THINKING")
                self.log("STATUS", "Processing command...", "status")
                actions = think(user_text)
                
                if not isinstance(actions, list):
                    actions = [actions]
                
                # Executing phase
                self.set_status("ACTIVE", "EXECUTING")
                for action in actions:
                    if not self.running:
                        break
                    self.execute_action(action)
                
                self.set_status("ACTIVE", "IDLE")

            except Exception as e:
                self.log("ERROR", str(e), "error")
                self.set_status("ERROR", "IDLE")
                time.sleep(0.5)
        
        # Clean shutdown
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.set_status("OFFLINE", "IDLE")
        speak("Code Nexus is now offline")

if __name__ == "__main__":
    app = EnhancedNexusUI()
    app.mainloop()
