# multi-ai-chat-manager - v1.0.0


[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/dhaneshbb/multi-ai-chat-manager/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-0078d4.svg)](https://github.com/dhaneshbb/multi-ai-chat-manager)
[![Python](https://img.shields.io/badge/python-3.7+-3776ab.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow.svg)



## What This Project Actually Does

Multi-AI Chat Manager solves the common problem of switching between ChatGPT, Claude, Gemini, Perplexity, Grok, and DeepSeek tabs when comparing responses. This Windows application launches your AI chat apps, arranges them in a neat grid on your screen, and lets you send prompts to selected AI applications with one click.

There are two pieces that work together:
1. **The main Python application** - Handles window management and selective message sending
2. **A Chrome extension** - Ensures reliable text pasting into AI chat input fields

## Overview

![Demo](./doc/videos/video.gif)

Multi-AI Chat Manager is a  productivity tool that allows users to send prompts to multiple AI applications simultaneously with selective targeting. The application features a clean, distraction-free interface optimized for  use.

## Key Features

- **Selective AI Targeting**: Choose specific AI applications to receive prompts
- **Interface**: Clean design without distracting elements  
- **Grid Window Management**: Automatic arrangement of AI windows
- **History Management**:  prompt history without navigation clutter
- **Chrome Extension Integration**: Reliable prompt delivery to web-based AIs
- **Multi-Monitor Support**: Configurable display preferences


## Complete Structure

```
Multi-AI Chat Manager /
├── .github/                       
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md      
│
├── doc/                         
│   ├── README.md                
│   ├── Installation.md          
│   ├── Usage.md                 
│   ├── SYSTEM_DIAGRAMS.md  
│   ├── diagrams/                
│   ├── images/                  
│   └── videos/                  
│
├── extensions/                  
│   └── Chrome/
│       ├── manifest.json        
│       ├── content.js           
│       └── README.md            
│
├── scripts/                     
│   ├── build_exe.py             
│   ├── run.bat                  
│   └── setup_config.py          
│
├── src/multi_ai_chat/           
│   ├── main.py                  
│   ├── config/
│   │   └── config.yml           
│   ├── core/                    
│   │   ├── input_history.py     
│   │   └── prompt_sender.py     
│   └── gui/                     
│       ├── interface.py         
│       └── window_manager.py    
│  
├── .gitignore                   
├── CHANGELOG.md                           
├── CONTRIBUTING.md             
├── DISCLAIMER.md               
├── LICENSE                    
├── manifest.json               
├── Readme.md                   
├── requirements.txt                          
└── SECURITY.md                 
```


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

## Workflow

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

## Installation Methods

### Pre-built Executable (Recommended)
1. Download release package
2. Extract to desired location
3. Install Chrome extension
4. Configure AI application shortcuts
5. Run executable

### Source Installation
```bash
# Clone repository
git clone https://github.com/dhaneshbb/multi-ai-chat-manager.git
cd multi-ai-chat-manager

# Install dependencies
pip install -r requirements.txt

# Configure applications
python scripts/setup_config.py

# Install Chrome extension manually

# Run application
python src/multi_ai_chat/main.py
```

## Build and Deployment

### Build Process

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

### Building Executable
```bash
python scripts/build_exe.py
```

Creates standalone executable with:
- All dependencies bundled
- Configuration files included
-  installer package
- Version information embedded

### Development Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest tests/

# Run application
python src/multi_ai_chat/main.py
```

### Chrome Extension Integration

The Chrome extension ensures reliable prompt delivery to web-based AI applications:

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

**Chrome Extension Features:**
- Universal compatibility across all supported AI platforms
- Smart detection of input fields (textarea vs contenteditable)
- SPA support for dynamic page changes
- Non-intrusive operation
-  error handling

## Usage Workflow

### Basic Operation
1. **Launch**: Start Multi-AI Chat Manager
2. **Initialize**: Wait for AI applications to load and arrange
3. **Select**: Choose target AI applications using checkboxes
4. **Prompt**: Enter prompt in main text area
5. **Send**: Press Enter or click send button
6. **Review**: Check responses in arranged AI windows

###  Workflows
- **Comparative Analysis**: Send same prompt to multiple AIs
- **Specialized Tasks**: Target specific AIs for their strengths
- **Batch Processing**: Process multiple prompts efficiently
- **Research Workflows**: Integrate with documentation tools

## Configuration Management

### AI Application Setup
```yaml
ai_apps:
  - name: "Claude"
    shortcut: "C:\\Program Files\\AI Apps\\Claude.lnk"
    keywords: ["claude"]
    enabled: true
    selected: true  # Default selection state
    priority: 0     # Grid position priority
```

### Configuration System Structure

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

### Display Configuration
```yaml
window:
  grid:
    cols: 3
    rows: 2
  display:
    preferred_display: 1
    use_work_area: true
```

### Timing Optimization
```yaml
window:
  timing:
    launch_delay: 0.1
    load_wait: 2.0
    prompt_send_delay: 0.1
```

## Troubleshooting

### Common Issues
- **AI Detection**: Verify shortcut paths and keywords
- **Prompt Delivery**: Ensure Chrome extension is installed
- **Window Management**: Run as Administrator if needed
- **Performance**: Adjust timing settings for slower systems

### Diagnostic Tools
- Configuration validator: `python scripts/setup_config.py`
- Log analysis: Check `logs/multi_ai_chat.log`
- Chrome extension: Browser console debugging

## Development Notes

### Code Organization

* **Modular Design**: Clear separation of concerns
* **Standards**: Follows PEP 8
* **Error Handling**: Robust exception management
* **Logging**: Detailed operational logs

### Extension Points

* **AI Platforms**: Configurable support
* **Grid Layouts**: Customizable arrangements
* **Themes**: Interface theming
* **Integrations**: External API hooks

## Security Considerations

### Data Privacy
- No data transmission to external servers
- Local storage only
- Configurable history retention
- User-controlled AI selection

### System Integration
- Windows API usage for window management
- Clipboard operations for prompt delivery
- File system access for configuration and logs
- Browser extension with minimal permissions


## License and Disclaimer

**License**: MIT License - Open source  tool

**Disclaimer**: Users are responsible for complying with AI platform Terms of Service. This tool is designed for legitimate research and productivity purposes.

## Support and Community

### Resources
- [Documentation](./doc):
  - [Installation](./doc/Installation.md)
  - [Usage](./doc/Usage.md)
  - [SYSTEM_DIAGRAMS](./doc/SYSTEM_DIAGRAMS.md)

- Example configurations
- Troubleshooting guides
- Video demonstrations

## Contributing

Contributions are welcome! Please read contributing guidelines and submit pull requests to GitHub repository see here [CONTRIBUTING.md](./CONTRIBUTING.md).

---

Multi-AI Chat Manager represents a  approach to AI chat management, focusing on productivity, reliability, and user control while maintaining clean, distraction-free operation.







