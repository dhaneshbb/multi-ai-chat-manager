# Multi-AI Chat Manager v1.0.0

 AI chat management tool for Windows that allows you to send prompts to multiple AI applications simultaneously with selective targeting capabilities.

<video width="640" controls>
  <source src="./doc/videos/video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


## Overview

Multi-AI Chat Manager solves the common problem of switching between multiple AI chat applications when comparing responses. It launches your AI applications, arranges them in a grid layout, and allows you to send prompts to selected AI models with a single click.

## Features

### Core Functionality
- **Selective AI Targeting**: Choose which AI applications receive your prompts using checkboxes
- **Interface**: Clean, distraction-free design optimized for productivity  
- **Grid Window Management**: Automatic arrangement of AI windows in customizable layouts
- **History Management**:  prompt history without navigation clutter
- **Chrome Extension Support**: Ensures reliable prompt delivery to web-based AI chats
- **Multi-Monitor Support**: Works with multiple display configurations

###  Design
- Normal window behavior (no always-on-top)
- Clean interface without cursor navigation
- Real-time status indicators
- Bulk selection controls (Select All/None)
- Error handling and recovery

## Supported AI Platforms

- ChatGPT
- Claude
- Google Gemini
- Perplexity
- Grok
- DeepSeek
- Microsoft Copilot (configurable)

## System Requirements

- Windows 10/11
- Python 3.8+ (for source installation)
- Google Chrome browser
- AI applications with valid desktop shortcuts

## Quick Start

### Option 1: Pre-built Executable
1. Download the latest release
2. Extract to desired location
3. Edit `config.yml` with your AI application shortcut paths
4. Install the Chrome extension from `extensions/Chrome/`
5. Run `Multi-AI Chat Manager.exe`

### Option 2: Source Installation
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure AI applications: `python scripts/setup_config.py`
4. Install Chrome extension
5. Run: `python src/multi_ai_chat/main.py`

## Configuration

Edit `src/multi_ai_chat/config/config.yml` to customize:

- AI application shortcuts and priorities
- Window grid layout (rows/columns)
- Display preferences
- Timing settings
- Default AI selection preferences

## Usage

1. **Launch**: Start the Multi-AI Chat Manager
2. **Select AIs**: Use checkboxes to choose which AI applications to target
3. **Enter Prompt**: Type your question in the main text area
4. **Send**: Press Enter or click "Send to Selected AI Apps"
5. **Manage Windows**: Use control buttons to minimize, maximize, or rearrange windows

## Project Structure

```
Multi-AI Chat Manager/
├── src/multi_ai_chat/         
│   ├── main.py                
│   ├── config/config.yml      
│   ├── core/                  
│   │   ├── prompt_sender.py   
│   │   └── input_history.py   
│   └── gui/                   
│       ├── interface.py       
│       └── window_manager.py  
├── extensions/Chrome/         
├── scripts/                   
├── data/                      
└── doc/                       
```

## Building from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AI applications
python scripts/setup_config.py

# Run from source
python src/multi_ai_chat/main.py

# Build executable
python scripts/build_exe.py
```

## Chrome Extension Installation

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `extensions/Chrome/` folder
5. Verify extension is enabled

## Troubleshooting

**AI apps not detected:**
- Verify shortcut paths in config.yml
- Run as Administrator if needed
- Check logs in `logs/multi_ai_chat.log`

**Prompts not sending:**
- Ensure Chrome extension is installed and enabled
- Check clipboard functionality
- Verify AI windows are responding

**Window arrangement issues:**
- Try running as Administrator
- Check display settings in config.yml
- Use "Maximize Grid" button multiple times if needed

## License

This project is open source under the MIT License. See LICENSE file for details.

## Support

- Check documentation in `doc/` folder
- Review logs in `logs/multi_ai_chat.log`
- Ensure all requirements are met
- Verify configuration settings

##  Use

This tool is designed for  productivity and research purposes. Users are responsible for complying with the Terms of Service of each AI platform they use.

---


Multi-AI Chat Manager v1.0.0 -  AI Chat Management Tool

