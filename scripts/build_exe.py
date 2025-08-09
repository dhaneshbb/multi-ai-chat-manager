#!/usr/bin/env python3
"""
Multi-AI Chat Manager v1.0.0 - Build Script
Creates a standalone executable with all dependencies and config files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'PyYAML',
        'psutil', 
        'pywin32',
        'pyinstaller'
    ]
    
    print("Checking dependencies...")
    
    for package in required_packages:
        try:
            if package == 'PyYAML':
                import yaml
            elif package == 'psutil':
                import psutil
            elif package == 'pywin32':
                import win32gui
            elif package == 'pyinstaller':
                import PyInstaller
            print(f"  {package} - OK")
        except ImportError:
            print(f"  {package} - Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"  {package} - Installed")
    
    print("All dependencies ready")
    return True

def create_version_info():
    """Create version info file"""
    version_content = '''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u' AI Tools'),
        StringStruct(u'FileDescription', u'Multi-AI Chat Manager'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'Multi-AI Chat Manager'),
        StringStruct(u'LegalCopyright', u'Copyright 2024'),
        StringStruct(u'OriginalFilename', u'Multi-AI Chat Manager.exe'),
        StringStruct(u'ProductName', u'Multi-AI Chat Manager'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    version_path = "data/version_info.txt"
    os.makedirs("data", exist_ok=True)
    
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(version_content)
    
    print("Version info file created")

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the directory containing this spec file
spec_dir = Path(SPECPATH)

# Define the main script and data files
main_script = spec_dir / 'src' / 'multi_ai_chat' / 'main.py'
config_dir = spec_dir / 'src' / 'multi_ai_chat' / 'config'

# Data files to include
datas = []
if config_dir.exists():
    datas.append((str(config_dir), 'config'))

# Hidden imports for all dependencies
hiddenimports = [
    'yaml',
    'PyYAML',
    'win32gui',
    'win32clipboard', 
    'win32con',
    'win32api',
    'win32process',
    'win32com.client',
    'psutil',
    'tkinter',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'threading',
    'logging',
    'time',
    'os',
    'sys',
    'pathlib'
]

# Analysis
a = Analysis(
    [str(main_script)],
    pathex=[str(spec_dir / 'src' / 'multi_ai_chat')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Bundle
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Multi-AI Chat Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='data/version_info.txt'
)
'''

    with open("multi_ai_chat.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("PyInstaller spec file created")

def verify_files():
    """Verify all required files exist"""
    required_files = [
        "src/multi_ai_chat/main.py",
        "src/multi_ai_chat/gui/interface.py",
        "src/multi_ai_chat/gui/window_manager.py", 
        "src/multi_ai_chat/core/prompt_sender.py",
        "src/multi_ai_chat/core/input_history.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False
    
    print("All required files found")
    
    # Check for config file
    config_files = [
        "config.yml",
        "src/multi_ai_chat/config/config.yml"
    ]
    
    config_found = any(os.path.exists(config_file) for config_file in config_files)
    
    if not config_found:
        print("WARNING: No config.yml found!")
        print("Expected locations:")
        for config_file in config_files:
            print(f"  - {config_file}")
        print("Run 'python scripts/setup_config.py' to create configuration")
        
        create_config = input("Create a basic config.yml now? (y/n): ").lower()
        if create_config == 'y':
            ensure_config_exists()
        else:
            print("Build will continue without config.yml")
            print("You must provide config.yml before running the application")
    
    return True

def ensure_config_exists():
    """Ensure config.yml exists"""
    config_path = "src/multi_ai_chat/config/config.yml"
    
    if not os.path.exists(config_path):
        print("Creating default config.yml...")
        default_config = '''# Multi-AI Chat Manager v1.0.0 Configuration
app:
  name: "Multi-AI Chat Manager"
  version: "1.0.0"

window:
  grid:
    cols: 3
    rows: 2
  display:
    auto_select: false
    preferred_display: 1
    use_work_area: true
  timing:
    launch_delay: 0.1
    load_wait: 2.0
    action_delay: 0.1
    prompt_send_delay: 0.1

ai_apps:
  - name: "ChatGPT"
    shortcut: "C:\\\\Path\\\\To\\\\ChatGPT.lnk"
    keywords: ["chatgpt", "chat.openai"]
    enabled: true
    selected: true
    priority: 5
    
  - name: "Claude" 
    shortcut: "C:\\\\Path\\\\To\\\\Claude.lnk"
    keywords: ["claude"]
    enabled: true
    selected: true
    priority: 0

gui:
  theme:
    bg_primary: "#1e1e1e"
    bg_secondary: "#2d2d2d"
    bg_input: "#404040"
    fg_primary: "#ffffff"
    fg_secondary: "#cccccc"
    accent_color: "#0078d4"
    success_color: "#4CAF50"
    warning_color: "#FF9800"
    error_color: "#f44336"
  
  window:
    width: 1000
    height: 700
    always_on_top: false
    resizable: true
  
  fonts:
    title: ["Segoe UI", 16, "bold"]
    normal: ["Segoe UI", 11]
    small: ["Segoe UI", 9]
    button: ["Segoe UI", 10]

history:
  max_entries: 100
  save_to_file: true
  history_file: "data/input_history.txt"
'''
        
        os.makedirs("src/multi_ai_chat/config", exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(default_config)
        
        print(f"Default config.yml created at {config_path}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            "multi_ai_chat.spec"
        ], capture_output=True, text=True, check=True)
        
        print("Build completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print("Build failed")
        print("Error output:")
        print(e.stderr)
        print("Stdout output:")
        print(e.stdout)
        return False

def create_distribution():
    """Create final distribution folder"""
    dist_folder = "dist"
    exe_name = "Multi-AI Chat Manager.exe"
    
    if not os.path.exists(os.path.join(dist_folder, exe_name)):
        print("Executable not found in dist folder")
        return False
    
    # Create distribution folder
    final_dist = "Multi-AI Chat Manager v1.0.0"
    if os.path.exists(final_dist):
        shutil.rmtree(final_dist)
    
    os.makedirs(final_dist)
    
    # Copy executable
    shutil.copy2(os.path.join(dist_folder, exe_name), final_dist)
    
    # Copy config file if it exists
    config_files = ["config.yml", "src/multi_ai_chat/config/config.yml"]
    config_copied = False
    
    for config_file in config_files:
        if os.path.exists(config_file):
            shutil.copy2(config_file, os.path.join(final_dist, "config.yml"))
            print(f"Copied config from: {config_file}")
            config_copied = True
            break
    
    if not config_copied:
        print("WARNING: No config.yml found to include in distribution")
        print("Users will need to create config.yml before running the application")
    
    # Create data directory
    data_dir = os.path.join(final_dist, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create readme
    readme_content = """Multi-AI Chat Manager v1.0.0

IMPORTANT SETUP REQUIRED:

1. CONFIGURATION: You MUST edit config.yml with your AI application shortcut paths
   - Update the 'shortcut' paths for each AI application
   - Adjust other settings as needed
   
2. CHROME EXTENSION: Install the Chrome extension for reliable operation
   - Go to chrome://extensions/
   - Enable Developer mode
   - Click "Load unpacked"
   - Select the extensions/Chrome folder

3. RUN APPLICATION: Double-click Multi-AI Chat Manager.exe

CONFIGURATION GUIDE:

Edit config.yml to update AI application shortcut paths:
- Find your AI app shortcuts (usually on Desktop or Start Menu)
- Copy the full path including .lnk extension
- Update the shortcut paths in config.yml

Example shortcut locations:
- Desktop: C:\\Users\\[Username]\\Desktop\\AppName.lnk
- Start Menu: C:\\Users\\[Username]\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\AppName.lnk

FEATURES:

- Select specific AI applications to send prompts to
-  interface without distracting elements
- Window management (minimize, maximize, arrange)
- Automatic window grid arrangement
- History management
- Always-on-top toggle option

USAGE:

- Select which AI applications to target using checkboxes
- Type prompts and press Enter to send to selected AIs
- Use buttons to manage windows (reopen, close, arrange)
-  interface designed for productivity

REQUIREMENTS:

- Windows 10/11
- AI applications installed with valid shortcuts
- Run as administrator if window management doesn't work
- Chrome extension for optimal prompt pasting

TROUBLESHOOTING:

- Check logs/multi_ai_chat.log for error details
- Verify AI application shortcuts exist and are correct
- Ensure Chrome extension is installed and enabled
- Run as administrator for window management features

For support, check the log file: logs/multi_ai_chat.log
"""
    
    readme_path = os.path.join(final_dist, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"Distribution created in '{final_dist}' folder")
    
    if not config_copied:
        print("\n" + "="*60)
        print("IMPORTANT: No config.yml included in distribution!")
        print("Users must create config.yml before running the application")
        print("Consider running: python scripts/setup_config.py")
        print("="*60)
    
    return True

def main():
    """Main build process"""
    print("Multi-AI Chat Manager v1.0.0 - Build Process")
    print("=" * 50)
    
    try:
        # Verify files exist
        if not verify_files():
            print("Build aborted - missing required files")
            return False
        
        # Check dependencies
        if not check_dependencies():
            print("Build aborted - dependency issues")
            return False
        
        # Ensure config exists
        ensure_config_exists()
        
        # Create build files
        create_version_info()
        create_spec_file()
        
        # Build executable
        if not build_executable():
            print("Build failed")
            return False
        
        # Create distribution
        if not create_distribution():
            print("Distribution creation failed")
            return False
        
        print("Build completed successfully")
        print("Test the executable in the distribution folder")
        print("Update config.yml with correct AI application paths")
        
        return True
        
    except Exception as e:
        print(f"Build error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("Build process failed")
    except KeyboardInterrupt:
        print("Build cancelled")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        input("Press Enter to exit...")