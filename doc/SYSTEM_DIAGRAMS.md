# Multi-AI Chat Manager v1.0.0

## System Architecture

```mermaid
graph TB
    subgraph DesktopApp["Python Desktop Application"]
        A["src/multi_ai_chat/main.py - Startup & Coordination"] --> B["src/multi_ai_chat/gui/window_manager.py - Window Control"]
        A --> C["src/multi_ai_chat/gui/interface.py - User Interface with AI Selection"]
        A --> D["src/multi_ai_chat/core/prompt_sender.py - Selective Message Automation"]
        A --> E["src/multi_ai_chat/core/input_history.py -  History Management"]
    end
    
    subgraph ChromeExt["Chrome Extension"]
        F["extensions/Chrome/manifest.json - Extension Config"] --> G["extensions/Chrome/content.js - Input Focus Handler"]
    end
    
    subgraph BuildTools["Build & Setup Tools"]
        H["scripts/build_exe.py - Executable Builder"]
        I["scripts/setup_config.py - Configuration Wizard"]
        J["data/version_info.txt - Version Information"]
    end
    
    subgraph AIApps["AI Applications with Selection Support"]
        K["ChatGPT - Priority 5 - Selectable"]
        L["Claude - Priority 0 - Selectable"]
        M["Google Gemini - Priority 1 - Selectable"]
        N["Perplexity - Priority 2 - Selectable"]
        O["Grok - Priority 3 - Selectable"]
        P["DeepSeek - Priority 4 - Selectable"]
    end
    
    subgraph ConfigData["Configuration & Data"]
        Q["src/multi_ai_chat/config/config.yml - Settings"]
        R["data/input_history.txt - Saved Prompts"]
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

##  Workflow

```mermaid
sequenceDiagram
    participant You
    participant MainApp as src/multi_ai_chat/main.py
    participant WindowMgr as gui/window_manager.py
    participant GUI as gui/interface.py
    participant Sender as core/prompt_sender.py
    participant Extension as Chrome Extension
    participant AIApps as Selected AI Applications
    participant History as core/input_history.py
    
    You->>MainApp: Launch Multi-AI Chat Manager 
    MainApp->>WindowMgr: Initialize window management
    MainApp->>GUI: Create  interface
    MainApp->>History: Load prompt history
    
    MainApp->>WindowMgr: Launch configured AI apps
    WindowMgr->>AIApps: Open applications using shortcuts
    WindowMgr->>WindowMgr: Detect and catalog windows
    WindowMgr->>AIApps: Arrange in custom grid layout
    WindowMgr-->>GUI: Update connection status
    
    You->>GUI: Select target AI applications via checkboxes
    You->>GUI: Enter prompt in text area
    You->>GUI: Press Enter to send
    GUI->>History: Save prompt to history
    GUI->>Sender: Send to selected AIs only
    
    loop For each selected AI application
        Sender->>AIApps: Focus selected window
        Sender->>AIApps: Copy prompt to clipboard
        Sender->>AIApps: Execute Ctrl+V
        Extension->>AIApps: Auto-focus input field
        AIApps->>AIApps: Paste and process prompt
        Sender->>AIApps: Execute Enter key
    end
    
    Sender-->>GUI: Report delivery status
    GUI-->>You: Display success/failure status
    
    You->>GUI: Use window management controls
    GUI->>WindowMgr: Execute minimize/maximize operations
    WindowMgr->>AIApps: Apply window state changes
```

## GUI Interface Layout 

```mermaid
graph TB
    subgraph GUILayout[" Interface Layout"]
        A2["Header Section - Title: Multi-AI Chat Manager  & Status"] --> B2["AI Selection Section - Checkboxes for Target Selection"]
        B2 --> C2["AI Status Row - Clickable Status Indicators"]
        C2 --> D2["Main Prompt Input -  ScrolledText Widget"]
        D2 --> E2["Control Panel - Send, Window Management Controls"]
        E2 --> F2["Status Bar -  Hotkeys Display"]
    end
    
    subgraph UserInteractions[" User Interactions"]
        G2["AI Selection - Checkbox Interface"] --> H2["Send Prompt - Enter Key Only"]
        H2 --> I2["Window Management -  Controls"]
        I2 --> J2["Individual App Focus - Click Status Indicators"]
    end
    
    subgraph VisualFeedback[" Visual Feedback"]
        K2["Real-time Status Updates"] --> L2["Selected AI Count Display"]
        L2 --> M2["App State Indicators -  Styling"]
        M2 --> N2["No Always-On-Top Behavior"]
    end
    
    A2 --> G2
    D2 --> H2
    E2 --> I2
    C2 --> J2
    
    H2 --> K2
    I2 --> K2
    J2 --> L2
```

**Interface Elements:**
- **Normal Window Behavior**: No always-on-top for  use
- **AI Selection Interface**: Checkbox-based targeting system
- **Clean Navigation**: No cursor up/down history navigation
- **Styling**: Dark theme with business-appropriate colors
- **Status Indicators**: Real-time feedback on AI application states

## Configuration System ()

```mermaid
graph TD
    A["src/multi_ai_chat/config/config.yml"] --> B["app"]
    A --> C["window"]
    A --> D["ai_apps"]
    A --> E["gui"]
    A --> F["history"]
    
    B --> B1["name: Multi-AI Chat Manager<br/>version: 1.0.0"]
    
    C --> C1["grid: cols 3, rows 2"]
    C --> C2["display: preferred_display 1"]
    C --> C3["timing:  delays"]
    
    D --> D1["6 AI Applications with Selection:"]
    D1 --> D2["Claude (priority 0, selected: true)"]
    D1 --> D3["Google Gemini (priority 1, selected: true)"]
    D1 --> D4["Perplexity (priority 2, selected: true)"]
    D1 --> D5["Grok (priority 3, selected: true)"]
    D1 --> D6["DeepSeek (priority 4, selected: true)"]
    D1 --> D7["ChatGPT (priority 5, selected: true)"]
    
    E --> E1["theme:  colors"]
    E --> E2["window: 1000×700, always_on_top: false"]
    E --> E3["fonts:  typography"]
    
    F --> F1["max_entries: 100<br/>save_to_file: true<br/>history_file: data/input_history.txt"]
```

##  Build Process

```mermaid
graph TD
    A7["Start Build Process"] --> B7["Check Dependencies: PyYAML, psutil, pywin32, pyinstaller"]
    B7 --> C7["Verify Required Files: src/multi_ai_chat structure"]
    C7 --> D7["Create data/version_info.txt for "]
    D7 --> E7["Generate PyInstaller Spec with new paths"]
    E7 --> F7["Run PyInstaller Build"]
    F7 --> G7["Create  Distribution"]
    
    subgraph Distribution[" Distribution Package"]
        H7["Multi-AI Chat Manager .exe"]
        I7["config.yml with AI selection support"]
        J7[" README.txt"]
        K7["data/ directory structure"]
        L7["Chrome Extension with updated manifest"]
    end
    
    G7 --> H7
    G7 --> I7
    G7 --> J7
    G7 --> K7
    G7 --> L7
```

## AI Selection Workflow

```mermaid
graph TD
    A8["Launch Application"] --> B8["Load AI Applications from Config"]
    B8 --> C8["Display Selection Interface"]
    C8 --> D8["User Selects Target AIs via Checkboxes"]
    
    D8 --> E8{"Any AIs Selected?"}
    E8 -->|No| F8["Show Warning: Select at least one AI"]
    E8 -->|Yes| G8["User Enters Prompt"]
    
    G8 --> H8["Press Enter to Send"]
    H8 --> I8["Filter Windows by Selected AIs"]
    I8 --> J8["Send Prompt to Selected AIs Only"]
    
    J8 --> K8["Display Results"]
    K8 --> L8["Update Status: Sent to X of Y selected AIs"]
    
    F8 --> C8
    L8 --> M8["Ready for Next Prompt"]
    M8 --> D8
```

##  Project Structure

```mermaid
graph TD
    A9["Multi-AI Chat Manager /"] --> B9["src/multi_ai_chat/"]
    A9 --> C9["extensions/Chrome/"]
    A9 --> D9["scripts/"]
    A9 --> E9["data/"]
    A9 --> F9["doc/"]
    A9 --> G9["logs/"]
    
    B9 --> B91["main.py -  Entry Point"]
    B9 --> B92["config/config.yml -  Configuration"]
    B9 --> B93["core/ - Core Business Logic"]
    B9 --> B94["gui/ -  Interface"]
    
    B93 --> B931["input_history.py -  History"]
    B93 --> B932["prompt_sender.py - Selective Targeting"]
    
    B94 --> B941["interface.py - AI Selection GUI"]
    B94 --> B942["window_manager.py -  Window Control"]
    
    C9 --> C91["manifest.json -  Extension Config"]
    C9 --> C92["content.js -  Input Focus"]
    C9 --> C93["README.md -  Documentation"]
    
    D9 --> D91["build_exe.py -  Builder"]
    D9 --> D92["setup_config.py - Configuration Wizard"]
    D9 --> D93["run.bat -  Launcher"]
    
    E9 --> E91["input_history.txt -  History Storage"]
    E9 --> E92["version_info.txt - Build Information"]
    
    F9 --> F91["README.md -  Documentation"]
    F9 --> F92["installation.md -  Setup Guide"]
    F9 --> F93["usage.md -  Usage Guide"]
    
    G9 --> G91["multi_ai_chat.log -  Logging"]
```

## Window Management States

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Launching: Load Configuration
    Launching --> Detecting: Start AI Applications
    Detecting --> Arranging: Find AI Windows
    Arranging --> Ready: Position in Grid
    
    Ready --> Minimized: Minimize All
    Minimized --> Ready: Maximize Grid
    
    Ready --> Focused: Individual App Focus
    Focused --> Ready: Focus Lost
    
    Ready --> Sending: Send to Selected AIs
    Sending --> Ready: Delivery Complete
    
    Ready --> Closing: Close All
    Closing --> [*]
    
    Ready --> Reopening: Reopen All
    Reopening --> Launching: Restart Process
```

## Chrome Extension Integration

```mermaid
graph TD
    A10["Ctrl+V Pressed in Browser"] --> B10{"In Input Field Already?"}
    B10 -->|Yes| C10["Allow Normal Paste - No Intervention"]
    B10 -->|No| D10["Execute AI Chat Input Detection"]
    
    D10 --> E10["Try Platform-Specific Selectors"]
    E10 --> F10{"Input Element Found?"}
    F10 -->|Yes| G10["Focus Input & Position Cursor"]
    F10 -->|No| H10["Try Generic Fallback Selectors"]
    
    H10 --> I10{"Any Input Found?"}
    I10 -->|Yes| G10
    I10 -->|No| J10["Silent Failure - No Disruption"]
    
    G10 --> K10["Ready for  Paste Operation"]
    K10 --> L10["Multi-AI Chat Manager Delivers Prompt"]
    
    C10 --> M10["Standard Browser Behavior"]
    J10 --> M10
    L10 --> M10
```

##  Use

This tool is designed for  productivity and research purposes. Users are 
responsible for complying with the Terms of Service of each AI platform they use.

---

Multi-AI Chat Manager v1.0.0 -  AI Chat Management Tool