# Code Nexus: Windows Voice Agent

## Important Legal Disclaimer
This software is provided strictly for **demonstration and educational purposes only**. Any commercial use, resale, or deployment in a production environment is strictly prohibited and may constitute a violation of applicable copyright and licensing laws. The authors and maintainers assume no liability for misuse of this code.

## Overview
Code Nexus is a sophisticated voice-controlled automation agent designed specifically for the Windows operating system. It leverages advanced language models via the Groq API to intepret user commands and execute complex tasks directly on the host machine.

The agent serves as a centralized control hub, allowing users to interact with their computer using natural language to perform file operations, control system settings, browse the web, and manage personal productivity tasks.

## Key Features
*   **System Control**: Manage volume, brightness, battery monitoring, and power operations (shutdown, restart).
*   **File Management**: Create, delete, rename, search, and organize files and directories verbally.
*   **Web Automation**: Perform Google searches, query Wikipedia, get weather updates, and read news.
*   **App Management**: Open and close applications by name.
*   **Productivity**: Set reminders, create notes, and manage clipboards.
*   **Visual Tools**: Take screenshots and manage image assets.
*   **Communication**: functionality to send WhatsApp messages.

## Prerequisites
*   Windows 10 or Windows 11
*   Python 3.8 or higher
*   A valid Groq API Key

## Installation

1.  Clone this repository to your local machine.
2.  Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_api_key_here
    ```

## Usage

### Command Line Interface
To run the agent in the terminal:
```bash
python main.py
```

### Graphical User Interface
To launch the agent with the modern GUI:
```bash
run_gui.bat
```
Or manually:
```bash
python gui.py
```

## Project Structure
*   `main.py`: The entry point for the command-line interface.
*   `gui.py`: The entry point for the graphical interface.
*   `core/`: Contains critical modules for listening, thinking (AI logic), and speaking.
*   `skills/`: A directory containing modular skills such as file management, browser control, and system hooks.
*   `scripts/`: Helper scripts for additional functionality.

## License
This project is unlicensed and reserved solely for private demonstration. All rights reserved.

---
**Developed by Code Nexus**
