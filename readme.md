# Multi-AI Chat Manager v2.0

## What This Project Actually Does

Hey! So I got tired of constantly switching between ChatGPT, Claude, Gemini, Perplexity, Grok, and DeepSeek tabs whenever I wanted to compare their responses to the same question. This Windows app basically solves that problem - it launches all your AI chat apps, arranges them in a neat grid on your screen, and lets you send the same prompt to all of them with just one click.

There are two pieces that work together:
1. **The main Python app** - Does all the heavy lifting with window management and sending your messages
2. **A little Chrome extension** - Makes sure your text actually gets pasted into the right chat boxes (trust me, this was needed!)

## Here's How It Actually Works

![Demo](./assets/video.gif)

*This GIF shows the whole workflow - I launch the app, it opens and arranges all the AI chat windows automatically, then I type a question once and boom, it goes to all of them. Pretty satisfying to watch, honestly.*

## Complete Project Structure

```
Multi-AI Chat Manager v2.0/
├── main.py                        # Application entry point
├── gui_interface.py               # Main user interface  
├── window_manager.py              # AI window detection & arrangement
├── prompt_sender.py               # Clipboard-based message sending
├── input_history.py               # Prompt history management
├── config.yml                     # Configuration file
├── requirements.txt               # Python dependencies
├── setup.py                       # Python package setup
├── manifest.json                  # Project metadata
├── readme.md                      # Main documentation
├── .gitignore                     # Git ignore patterns
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history
├── CODE_OF_CONDUCT.md             # Community guidelines
├── CONTRIBUTING.md                # Contribution guide
├── DISCLAIMER.md                  # Usage disclaimer
├── ROADMAP.md                     # Future development plans
├── SECURITY.md                    # Security policy
│
├── .github/                       # GitHub templates
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
│
├── assets/
│   ├── desktop.png
│   ├── video.gif
│   └── diagram.svg
│
├── Chrome Extension/              # Browser extension
│   ├── manifest.json             # Extension configuration
│   └── content.js                # Auto-focus script
│
├── Build Tools/
│   ├── build_exe.py               # Creates standalone executable
│   ├── setup_config.py
│   ├── test_fixes.py
│   └── version_info.txt
```

## System Architecture

```mermaid
graph TB
    subgraph DesktopApp["Python Desktop Application"]
        A["main.py - Startup & Coordination"] --> B["window_manager.py - Window Control"]
        A --> C["gui_interface.py - User Interface"]
        A --> D["prompt_sender.py - Message Automation"]
        A --> E["input_history.py - History Management"]
    end
    
    subgraph ChromeExt["Chrome Extension"]
        F["manifest.json - Extension Config"] --> G["content.js - Input Focus Handler"]
    end
    
    subgraph BuildTools["Build & Setup Tools"]
        H["build_exe.py - Executable Builder"]
        I["setup_config.py - Configuration Wizard"]
        J["test_fixes.py - System Diagnostics"]
    end
    
    subgraph AIApps["AI Applications"]
        K["ChatGPT - Priority 5"]
        L["Claude - Priority 0"]
        M["Google Gemini - Priority 1"]
        N["Perplexity - Priority 2"]
        O["Grok - Priority 3"]
        P["DeepSeek - Priority 4"]
    end
    
    subgraph ConfigData["Configuration & Data"]
        Q["config.yml - Settings"]
        R["input_history.txt - Saved Prompts"]
    end
    
    B --> K
    B --> L
    B --> M
    B --> N
    B --> O
    B --> P
    
    D --> K
    D --> L
    D --> M
    D --> N
    D --> O
    D --> P
    
    G --> K
    G --> L
    G --> M
    G --> N
    G --> O
    G --> P
    
    A --> Q
    E --> R
```

## How I Built This To Work

```mermaid
sequenceDiagram
    participant You
    participant MainApp as main.py
    participant WindowMgr as window_manager.py
    participant GUI as gui_interface.py
    participant Sender as prompt_sender.py
    participant Extension as Chrome Extension
    participant AIApps as AI Applications
    participant History as input_history.py
    
    You->>MainApp: Double-click to start
    MainApp->>WindowMgr: Get the window manager ready
    MainApp->>GUI: Build the interface
    MainApp->>History: Load your old messages
    
    MainApp->>WindowMgr: Start launching AI apps
    WindowMgr->>AIApps: Open apps using your shortcuts
    WindowMgr->>WindowMgr: Find their windows
    WindowMgr->>AIApps: Arrange them in the 3x2 grid
    WindowMgr-->>GUI: Tell interface how many we found
    
    You->>GUI: Type your question and hit Enter
    GUI->>History: Save this so you can find it later
    GUI->>Sender: Send this to everyone
    
    loop For each AI app window
        Sender->>AIApps: Click on the window
        Sender->>AIApps: Copy your text to clipboard
        Sender->>AIApps: Press Ctrl+V
        Extension->>AIApps: Focus the right input box
        AIApps->>AIApps: Text gets pasted
        Sender->>AIApps: Hit Enter to send
    end
    
    Sender-->>GUI: Report back how it went
    GUI-->>You: Show you the status
    
    You->>GUI: Click minimize
    GUI->>WindowMgr: Hide all the windows
    WindowMgr->>AIApps: Minimize yourselves
    
    You->>GUI: Click maximize grid
    GUI->>WindowMgr: Bring everything back
    WindowMgr->>AIApps: Come back up
    WindowMgr->>AIApps: Get back in your positions
```

## The Main Parts (What Actually Does What)

### 1. The Startup Process (main.py)

```mermaid
graph TD
    A["You start the app"] --> B["Check if everything's installed"]
    B --> C["Make sure we can find your AI apps"]
    C --> D["Load your settings"]
    D --> E["Start up all the pieces"]
    E --> F["Create the interface"]
    F --> G["Launch your AI apps in background"]
    
    G --> H["Open all AI applications"]
    H --> I["Find their windows"]
    I --> J["Arrange them nicely"]
    J --> K["Tell you we're ready"]
```

This is where it all begins. I spent way too much time making sure this doesn't crash if something goes wrong - like if one of your AI app shortcuts is broken, it'll just tell you what's up and keep going with the others instead of dying completely.

### 2. Window Manager (window_manager.py)

```mermaid
graph TB
    subgraph WindowDetection["AI Window Detection"]
        A1["Enumerate All Windows"] --> B1["Check Window Titles"]
        B1 --> C1["Match Against Keywords"]
        C1 --> D1["Validate as AI App"]
        D1 --> E1["Store Window Information"]
    end
    
    subgraph DisplayManagement["Display & Layout"]
        F1["Detect Available Monitors"] --> G1["Select Preferred Display"]
        G1 --> H1["Calculate 3x2 Grid Positions"]
        H1 --> I1["Apply Custom App Priorities"]
    end
    
    subgraph WindowOperations["Window Operations"]
        J1["Launch Applications"] --> K1["Arrange in Grid"]
        K1 --> L1["Minimize/Restore All"]
        L1 --> M1["Individual App Focus"]
        M1 --> N1["Close All Apps"]
    end
    
    E1 --> J1
    I1 --> K1
```

**Custom App Priority Order (from config.yml):**
- Position 0: Claude (priority 0)
- Position 1: Google Gemini (priority 1) 
- Position 2: Perplexity (priority 2)
- Position 3: Grok (priority 3)
- Position 4: DeepSeek (priority 4)
- Position 5: ChatGPT (priority 5)

**Key Features:**
- Multi-monitor support with preferred display selection
- Multiple window positioning methods for reliability
- Taskbar icon management (hide AI apps from taskbar)
- Window state validation and recovery
- Custom grid arrangement based on priority

### 3. GUI Interface (gui_interface.py)

```mermaid
graph TB
    subgraph GUILayout["Interface Layout"]
        A2["Header Section - Title & Status"] --> B2["AI App Icons Row - Clickable Buttons"]
        B2 --> C2["Main Prompt Input - ScrolledText Widget"]
        C2 --> D2["Control Button Row - Send, History, Window Controls"]
        D2 --> E2["Status Bar - Hotkeys & Version"]
    end
    
    subgraph UserInteractions["User Interactions"]
        F2["Send Prompt - Enter Key"] --> G2["History Navigation - Up/Down Arrows"]
        G2 --> H2["Window Management - Minimize/Maximize"]
        H2 --> I2["Individual App Control - Click App Icons"]
    end
    
    subgraph VisualFeedback["Visual Feedback"]
        J2["Real-time Status Updates"] --> K2["Window Count Display"]
        K2 --> L2["App State Indicators - Minimized/Active"]
    end
    
    A2 --> F2
    C2 --> F2
    D2 --> H2
    B2 --> I2
    
    F2 --> J2
    H2 --> J2
    I2 --> L2
```

**Interface Elements:**
- **Dark theme** with professional color scheme
- **Always on top** option to stay visible
- **Individual AI app buttons** showing minimized state
- **Keyboard shortcuts** for power users
- **Real-time status updates** with color coding

### 4. Prompt Sender (prompt_sender.py)

```mermaid
graph LR
    A3["Receive Prompt"] --> B3["Store Current Focus"]
    B3 --> C3["Start AI App Loop"]
    C3 --> D3["Bring Window to Front using SetForegroundWindow"]
    D3 --> E3["Copy to Clipboard using win32clipboard"]
    E3 --> F3["Simulate Ctrl+V using WScript.Shell"]
    F3 --> G3["Wait for Extension Input Focus"]
    G3 --> H3["Simulate Enter Key"]
    H3 --> I3["Wait & Next App with 1 second delay"]
    I3 --> C3
    C3 --> J3["All Apps Complete"]
    J3 --> K3["Restore Original Focus"]
```

**Technical Implementation:**
- Uses Windows API (win32gui, win32clipboard)
- COM automation via WScript.Shell
- Configurable delays between operations
- Error handling with graceful failure
- Focus restoration to prevent disruption

### 5. Input History (input_history.py)

```mermaid
graph TD
    A4["New Prompt Entered"] --> B4{"Duplicate of Last?"}
    B4 -->|Yes| C4["Skip Adding"]
    B4 -->|No| D4["Add to History List"]
    
    D4 --> E4["Maintain Max 100 Entries"]
    E4 --> F4["Save to input_history.txt with timestamp"]
    
    G4["User Presses Up/Down"] --> H4{"Direction?"}
    H4 -->|Up| I4["Get Previous Entry"]
    H4 -->|Down| J4["Get Next Entry"]
    
    I4 --> K4["Update GUI Text"]
    J4 --> K4
    K4 --> L4["Position Cursor at End"]
```

**File Format (input_history.txt):**
```
2025-07-29T09:00:22.141309 | Tell me a random fact, then link it to something surprising.
2025-07-28T18:08:34.151282 | higher index compared to other countries
```

### 6. Chrome Extension (manifest.json + content.js)

```mermaid
graph TD
    A5["Ctrl+V Pressed in Browser"] --> B5{"Already in Input Field?"}
    B5 -->|Yes| C5["Allow Normal Paste"]
    B5 -->|No| D5["Find AI Chat Input"]
    
    D5 --> E5["Try Platform-Specific Selectors"]
    E5 --> F5{"Input Found?"}
    F5 -->|Yes| G5["Focus Input Element"]
    F5 -->|No| H5["Try Generic Selectors"]
    
    H5 --> I5{"Found Anything?"}
    I5 -->|Yes| G5
    I5 -->|No| J5["Silent Failure"]
    
    G5 --> K5["Set Cursor to End"]
    K5 --> L5["Ready for Paste"]
```

**Platform-Specific Selectors:**
```javascript
// ChatGPT
'#prompt-textarea'
'textarea[data-id="root"]'

// Claude  
'div[contenteditable="true"][data-testid="composer-input"]'

// Gemini
'textarea[placeholder*="Enter a prompt"]'

// Perplexity
'textarea[placeholder*="Ask anything"]'

// Grok
'textarea[placeholder*="Ask Grok"]'

// DeepSeek
'textarea[placeholder*="Send a message"]'
```

**Extension Features:**
- **Universal compatibility** across all major AI platforms
- **Smart detection** of input fields (textarea vs contenteditable)
- **SPA support** handles dynamic page changes
- **Non-intrusive** only activates when needed
- **Debug logging** for troubleshooting

## Configuration System (config.yml)

```mermaid
graph TD
    A["config.yml"] --> B["app"]
    A --> C["window"]
    A --> D["ai_apps"]
    A --> E["gui"]
    A --> F["history"]
    A --> G["taskbar"]
    
    B --> B1["name: Multi-AI Chat Manager<br/>version: 2.0.0"]
    
    C --> C1["grid: cols 3, rows 2"]
    C --> C2["display: preferred_display 2"]
    C --> C3["timing: 4 delay settings"]
    
    D --> D1["6 AI Applications:"]
    D1 --> D2["Claude (priority 0)"]
    D1 --> D3["Google Gemini (priority 1)"]
    D1 --> D4["Perplexity (priority 2)"]
    D1 --> D5["Grok (priority 3)"]
    D1 --> D6["DeepSeek (priority 4)"]
    D1 --> D7["ChatGPT (priority 5)"]
    
    E --> E1["theme: 9 colors"]
    E --> E2["window: 1000×600"]
    E --> E3["fonts: 4 types"]
    
    F --> F1["max_entries: 100<br/>save_to_file: true"]
    
    G --> G1["hide_ai_apps: true<br/>show_only_manager: true"]
```

**Grid Layout Visualization (from config.yml):**
```
# Grid Position Layout (3×2):
# Row 1: Claude, Google Gemini, Perplexity  
# Row 2: Grok, DeepSeek, ChatGPT
Display: Monitor 2 (preferred_display: 2)
Window Size: 1000×600 pixels per grid cell

```

**AI Applications Configuration Details:**
```yaml
# Each AI app in the config.yml has this structure:
- name: "Claude"
  shortcut: "C:\\Program Files\\chat_ai\\ai dhaneshbb\\dhaneshbb5_Claude.lnk"
  keywords: ["claude"]
  enabled: true
  priority: 0
```

## Build and Deployment

### Build Process (build_exe.py)

```mermaid
graph TD
    A7["Start Build Process"] --> B7["Check Dependencies: PyYAML, psutil, pywin32, pyinstaller"]
    B7 --> C7["Verify Required Files: main.py, gui_interface.py, etc."]
    C7 --> D7["Create version_info.txt"]
    D7 --> E7["Generate PyInstaller Spec"]
    E7 --> F7["Run PyInstaller Build"]
    F7 --> G7["Create Distribution Folder"]
    
    subgraph Distribution["Final Package"]
        H7["Multi-AI Chat Manager.exe"]
        I7["config.yml"]
        J7["README.txt"]
    end
    
    G7 --> H7
    G7 --> I7
    G7 --> J7
```

### System Requirements

**For Python Development:**
```
Python 3.8+
PyYAML>=6.0          # Configuration file parsing
psutil>=5.9.0        # Process management
pywin32>=306         # Windows API integration
pyinstaller>=6.0     # Executable building
```

**For End Users:**
- Windows 10/11
- Google Chrome browser
- AI chat applications installed

## Installation Guide

### 1. Download and Setup
```bash
# Clone or download the project
git clone https://github.com/dhaneshbb/multi-ai-chat-manager.git
cd multi-ai-chat-manager

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the folder containing `manifest.json` and `content.js`
5. Verify extension appears in extensions list

### 3. Configure AI Applications
```bash
# Run interactive configuration
python setup_config.py
```
This will:
- Search for AI app shortcuts automatically
- Let you select which apps to include
- Create/update config.yml with correct paths

### 4. Test System
```bash
# Run diagnostics
python test_fixes.py
```
Checks:
- All dependencies installed
- Config file valid
- Clipboard functionality
- Window detection capabilities
- COM automation working

### 5. Launch Application
```bash
# Run from source
python main.py

# OR build standalone executable
python build_exe.py
```

## Usage Instructions

### Basic Workflow
1. **Launch** the Multi-AI Chat Manager
2. **Wait** for AI applications to start and arrange automatically
3. **Type** your prompt in the main text area
4. **Press Enter** or click "Send to All AI Apps"
5. **Watch** as your prompt appears in all AI chat windows
6. **Compare** responses from different AI models

### Keyboard Shortcuts
- **Enter**: Send prompt to all AI apps
- **Shift+Enter**: New line in prompt (for longer messages)
- **Up Arrow**: Navigate to previous prompt in history
- **Down Arrow**: Navigate to next prompt in history

### Window Management
- **Minimize All**: Hide all AI windows (keeps them running)
- **Maximize Grid**: Restore minimized windows and arrange in grid
- **Reopen All**: Close all AI apps and restart them
- **Close All**: Shut down all AI applications
- **Individual App Buttons**: Click to bring specific AI app to front

## Troubleshooting

### Common Issues and Solutions

**"AI apps aren't being detected!"**
- Check shortcut paths in config.yml are correct
- Verify AI apps are actually launching
- Look at app keywords - they must match window titles
- Run `python test_fixes.py` to diagnose

**"Windows won't arrange properly!"**
- Run as Administrator (Windows UAC can block window operations)
- Check display settings in config.yml 
- Some apps resist window manipulation - that's normal
- Try the "Maximize Grid" button multiple times

**"Prompts aren't sending!"**
- **Most common**: Chrome extension not installed/enabled
- Test manual copy/paste in AI apps
- Check clipboard functionality with test_fixes.py
- Verify windows are actually getting focus
- Enterprise security software may block automation

**"Chrome extension not working!"**
- Verify enabled at `chrome://extensions/`
- Check browser console (F12) for errors
- Refresh AI chat pages after installing extension
- Extension doesn't work in incognito mode
- AI sites may have changed their input selectors

**"Everything is broken!"**
```bash
python test_fixes.py
```
This diagnostic script will identify specific problems and suggest fixes.

## Advanced Configuration

### Custom AI App Setup
Edit config.yml to add new AI platforms:
```yaml
ai_apps:
  - name: "New AI App"
    shortcut: "C:\\Path\\To\\App.lnk"
    keywords: ["newai", "custom"]
    enabled: true
    priority: 6
```

### Grid Layout Customization
```yaml
window:
  grid:
    cols: 2    # Change to 2x3 layout
    rows: 3
  display:
    preferred_display: 1  # Use primary monitor
```

### Timing Adjustments
```yaml
window:
  timing:
    launch_delay: 0.5      # Slower app launching
    load_wait: 3.0         # More time for apps to load
    prompt_send_delay: 0.2 # Slower prompt sending
```

## Technical Architecture

### Class Structure

**WindowManager** (window_manager.py)
- `detect_displays()` → Find available monitors
- `launch_apps_parallel()` → Start all configured AI apps
- `get_ai_windows_fast()` → Detect AI application windows
- `arrange_windows_grid()` → Position windows in custom grid
- `minimize_all_windows()` → Hide all AI apps
- `restore_all_windows()` → Restore minimized windows
- `close_all_windows()` → Shut down AI applications

**PromptSender** (prompt_sender.py)
- `send_prompt_to_all()` → Main prompt distribution function
- `_send_prompt_to_window()` → Send to individual window
- `_restore_original_focus()` → Return focus to original window

**CleanGUI** (gui_interface.py)
- `create_gui()` → Build tkinter interface
- `update_status()` → Update status messages
- `update_window_count()` → Update AI app counter
- `_on_send_prompt()` → Handle prompt sending
- `_create_app_icons()` → Generate clickable app buttons

**InputHistoryManager** (input_history.py)
- `add_entry()` → Save new prompt to history
- `get_previous()` → Navigate backward in history
- `get_next()` → Navigate forward in history
- `get_stats()` → History usage statistics

### Chrome Extension API

**content.js Functions:**
- `getPlatformName()` → Identify current AI platform
- `findInput()` → Locate chat input element
- `focusInput()` → Focus input and position cursor
- `handleKeyDown()` → Process Ctrl+V keypress
- `isInInputField()` → Check if already typing

## Known Limitations

1. **Windows-only** - Uses Windows-specific APIs
2. **Chrome dependency** - Extension requires Chrome browser
3. **Shortcut-based launching** - Needs valid .lnk files
4. **Window title sensitivity** - AI apps changing titles can break detection
5. **UAC interference** - May need Administrator privileges
6. **Antivirus false positives** - Automation features may trigger security software
7. **SPA complexity** - Some AI sites with complex JavaScript may be unreliable

## Development Notes

### Contributing Guidelines
- Follow Python PEP 8 conventions
- Add comprehensive logging for debugging
- Test on multiple Windows versions
- Update Chrome extension selectors when AI sites change
- Maintain backward compatibility with existing configs

### Future Improvements
- Support for additional AI platforms
- Firefox extension version
- Cross-platform support (Mac/Linux)
- API-based integration (when available)
- Advanced prompt templating
- Response comparison features

---

## License and Disclaimer

This project is open source under the MIT License. 

**IMPORTANT**: Users are responsible for complying with AI platform Terms of Service. 
See DISCLAIMER.md for full details.

---

*This documentation represents the complete Multi-AI Chat Manager v2.0 system as implemented. Built to solve the daily problem of comparing AI responses efficiently.*
