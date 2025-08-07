# Installation Guide - Multi-AI Chat Manager v1.0.0

This guide covers installation methods for the Multi-AI Chat Manager tool.

## Installation Methods

### Method 1: Pre-built Executable (Recommended)

#### Requirements
- Windows 10/11
- Google Chrome browser
- AI applications with desktop shortcuts

#### Steps
1. **Download Release**
   - Download the latest release package
   - Extract to your preferred location (e.g., `C:\Program Files\Multi-AI Chat Manager\`)

2. **Install Chrome Extension**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extensions/Chrome/` folder
   - Verify the extension appears as enabled

3. **Configure AI Applications**
   - Edit `config.yml` in the application folder
   - Update shortcut paths for your AI applications
   - Adjust settings as needed

4. **First Run**
   - Run `Multi-AI Chat Manager.exe`
   - Allow Windows Defender/antivirus if prompted
   - The application will launch and arrange your AI windows

### Method 2: Source Installation

#### Requirements
- Windows 10/11
- Python 3.8 or higher
- pip package manager
- Google Chrome browser

#### Steps
1. **Clone Repository**
   ```bash
   git clone https://github.com/dhaneshbb/multi-ai-chat-manager.git
   cd multi-ai-chat-manager
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome Extension**
   - Open Chrome → `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `extensions/Chrome/` folder

4. **Configure Application**
   ```bash
   python scripts/setup_config.py
   ```
   Follow the interactive prompts to configure your AI applications.

5. **Run Application**
   ```bash
   python src/multi_ai_chat/main.py
   ```

#### Building Executable (Optional)
```bash
python scripts/build_exe.py
```

## Configuration Setup

### Automatic Configuration
Run the setup helper for guided configuration:
```bash
python scripts/setup_config.py
```

### Manual Configuration
Edit `src/multi_ai_chat/config/config.yml`:

```yaml
ai_apps:
  - name: "ChatGPT"
    shortcut: "C:\\Path\\To\\ChatGPT.lnk"
    keywords: ["chatgpt", "chat.openai"]
    enabled: true
    selected: true
    priority: 5
    
  - name: "Claude"
    shortcut: "C:\\Path\\To\\Claude.lnk"
    keywords: ["claude"]
    enabled: true
    selected: true
    priority: 0
```

### Finding Shortcut Paths
AI application shortcuts are typically located in:
- Desktop: `C:\Users\[Username]\Desktop\`
- Start Menu: `C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\`
- Public: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\`

## Verification

### Test Installation
1. Launch Multi-AI Chat Manager
2. Verify AI applications open and arrange in grid
3. Test prompt sending to selected applications
4. Check Chrome extension functionality

### Diagnostic Tools
```bash
# Run diagnostics
python scripts/setup_config.py
# Select option 2: Validate Existing Configuration
```

## Troubleshooting Installation

### Common Issues

**Python/Dependencies**
- Ensure Python 3.8+ is installed
- Use `pip install --upgrade pip` before installing dependencies
- Install Visual C++ Redistributable if pywin32 fails

**Chrome Extension**
- Verify Developer mode is enabled
- Extension must be "unpacked" not packaged
- Refresh AI chat pages after installation

**AI Application Detection**
- Shortcut paths must be exact (including .lnk extension)
- Test shortcuts manually by double-clicking
- Use absolute paths, not relative paths

**Permissions**
- Run as Administrator if window management fails
- Allow application through Windows Defender
- Disable antivirus temporarily if needed during first run

### Error Resolution

**"Module not found" errors:**
```bash
pip install --force-reinstall -r requirements.txt
```

**"Access denied" errors:**
```bash
# Run Command Prompt as Administrator
pip install -r requirements.txt
```

**Window arrangement failures:**
- Update display settings in config.yml
- Try running as Administrator
- Check if AI applications allow window manipulation

## Advanced Installation

### Custom Python Environment
```bash
# Create virtual environment
python -m venv multi_ai_env
multi_ai_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Portable Installation
1. Install Python portable version
2. Create folder structure matching project layout
3. Install dependencies to local folder
4. Use relative paths in configuration

### Enterprise Installation
- Use centralized configuration management
- Deploy Chrome extension via Group Policy
- Customize shortcuts for standard AI application installations
- Configure logging paths for monitoring

## Uninstallation

### Remove Application
1. Close Multi-AI Chat Manager
2. Delete application folder
3. Remove Chrome extension from `chrome://extensions/`
4. Delete data folder if desired

### Clean Registry (if needed)
- No registry modifications are made by default
- Only remove if you enabled specific Windows integrations

## Next Steps

After successful installation:
1. Review [Usage Guide](usage.md)
2. Customize configuration for your workflow
3. Set up keyboard shortcuts if desired
4. Configure AI application preferences

---

For additional support, check the troubleshooting section or review log files in the `logs/` directory.