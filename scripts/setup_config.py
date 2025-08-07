#!/usr/bin/env python3
"""
Multi-AI Chat Manager v1.0.0 - Configuration Setup Helper
 configuration tool for AI application shortcuts
"""

import os
import yaml
from pathlib import Path

def find_ai_shortcuts():
    """Find potential AI application shortcuts on the system"""
    potential_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"),
        "C:/ProgramData/Microsoft/Windows/Start Menu/Programs",
        "C:/Users/Public/Desktop"
    ]
    
    ai_keywords = [
        'chatgpt', 'chat gpt', 'openai',
        'claude', 'anthropic',
        'gemini', 'bard', 'google ai',
        'perplexity',
        'grok', 'x.ai',
        'deepseek',
        'copilot',
        'bing chat'
    ]
    
    found_shortcuts = []
    
    for search_path in potential_paths:
        if not os.path.exists(search_path):
            continue
            
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.lower().endswith('.lnk'):
                        file_lower = file.lower()
                        for keyword in ai_keywords:
                            if keyword in file_lower:
                                full_path = os.path.join(root, file)
                                found_shortcuts.append({
                                    'name': file[:-4],  # Remove .lnk extension
                                    'path': full_path,
                                    'keyword': keyword
                                })
                                break
        except (PermissionError, OSError):
            continue
    
    return found_shortcuts

def detect_ai_app_type(name, path):
    """Detect the type of AI application based on name/path"""
    name_lower = name.lower()
    
    if any(keyword in name_lower for keyword in ['chatgpt', 'chat gpt', 'openai']):
        return {
            'name': 'ChatGPT',
            'keywords': ['chatgpt', 'chat.openai', 'openai'],
            'priority': 5
        }
    elif any(keyword in name_lower for keyword in ['claude', 'anthropic']):
        return {
            'name': 'Claude',
            'keywords': ['claude', 'anthropic'],
            'priority': 0
        }
    elif any(keyword in name_lower for keyword in ['gemini', 'bard']):
        return {
            'name': 'Google Gemini',
            'keywords': ['gemini', 'bard', 'google'],
            'priority': 1
        }
    elif 'perplexity' in name_lower:
        return {
            'name': 'Perplexity',
            'keywords': ['perplexity'],
            'priority': 2
        }
    elif any(keyword in name_lower for keyword in ['grok', 'x.ai']):
        return {
            'name': 'Grok',
            'keywords': ['grok', 'x.ai'],
            'priority': 3
        }
    elif 'deepseek' in name_lower:
        return {
            'name': 'DeepSeek',
            'keywords': ['deepseek'],
            'priority': 4
        }
    elif any(keyword in name_lower for keyword in ['copilot', 'bing']):
        return {
            'name': 'Microsoft Copilot',
            'keywords': ['copilot', 'bing'],
            'priority': 6
        }
    else:
        return {
            'name': name,
            'keywords': [name_lower.replace(' ', '')],
            'priority': 999
        }

def create_ai_app_config(shortcuts):
    """Create AI app configuration from found shortcuts"""
    ai_apps = []
    
    for shortcut in shortcuts:
        app_info = detect_ai_app_type(shortcut['name'], shortcut['path'])
        
        ai_app = {
            'name': app_info['name'],
            'shortcut': shortcut['path'],
            'keywords': app_info['keywords'],
            'enabled': True,
            'selected': True,
            'priority': app_info['priority']
        }
        
        ai_apps.append(ai_app)
    
    # Sort by priority
    ai_apps.sort(key=lambda x: x['priority'])
    
    return ai_apps

def load_existing_config():
    """Load existing configuration if it exists"""
    config_path = "src/multi_ai_chat/config/config.yml"
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading existing config: {e}")
            return None
    return None

def save_config(config):
    """Save configuration to file"""
    try:
        config_dir = "src/multi_ai_chat/config"
        os.makedirs(config_dir, exist_ok=True)
        
        config_path = os.path.join(config_dir, "config.yml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def create_default_config():
    """Create default configuration structure"""
    return {
        'app': {
            'name': 'Multi-AI Chat Manager',
            'version': '1.0.0'
        },
        'window': {
            'grid': {'cols': 3, 'rows': 2},
            'display': {
                'auto_select': False,
                'preferred_display': 1,
                'use_work_area': True
            },
            'timing': {
                'launch_delay': 0.1,
                'load_wait': 2.0,
                'action_delay': 0.1,
                'prompt_send_delay': 0.1
            }
        },
        'gui': {
            'theme': {
                'bg_primary': '#1e1e1e',
                'bg_secondary': '#2d2d2d',
                'bg_input': '#404040',
                'fg_primary': '#ffffff',
                'fg_secondary': '#cccccc',
                'accent_color': '#0078d4',
                'success_color': '#4CAF50',
                'warning_color': '#FF9800',
                'error_color': '#f44336'
            },
            'window': {
                'width': 1000,
                'height': 700,
                'always_on_top': False,
                'resizable': True
            },
            'fonts': {
                'title': ['Segoe UI', 16, 'bold'],
                'normal': ['Segoe UI', 11],
                'small': ['Segoe UI', 9],
                'button': ['Segoe UI', 10]
            }
        },
        'history': {
            'max_entries': 100,
            'save_to_file': True,
            'history_file': 'data/input_history.txt'
        }
    }

def interactive_setup():
    """Interactive configuration setup"""
    print("Multi-AI Chat Manager v1.0.0 - Configuration Helper")
    print("=" * 60)
    
    # Search for shortcuts
    print("Searching for AI application shortcuts...")
    shortcuts = find_ai_shortcuts()
    
    if shortcuts:
        print(f"Found {len(shortcuts)} potential AI application shortcuts:")
        for i, shortcut in enumerate(shortcuts, 1):
            print(f"  {i}. {shortcut['name']} -> {shortcut['path']}")
    else:
        print("No AI application shortcuts found automatically")
        print("You can manually add them later in config.yml")
    
    # Load or create config
    config = load_existing_config()
    if config:
        print("\nFound existing config.yml")
        update = input("Do you want to update it with found shortcuts? (y/n): ").lower()
        if update != 'y':
            print("Configuration unchanged")
            return
    else:
        print("\nCreating new configuration...")
        config = create_default_config()
    
    # Configure AI apps
    if shortcuts:
        print("\nConfiguring AI applications...")
        
        selected_shortcuts = []
        for i, shortcut in enumerate(shortcuts, 1):
            use_app = input(f"Include {shortcut['name']}? (y/n): ").lower()
            if use_app == 'y':
                selected_shortcuts.append(shortcut)
        
        if selected_shortcuts:
            config['ai_apps'] = create_ai_app_config(selected_shortcuts)
            print(f"Configured {len(selected_shortcuts)} AI applications")
        else:
            config['ai_apps'] = []
            print("No AI applications selected")
    else:
        # Manual configuration
        print("\nManual AI application configuration:")
        ai_apps = []
        
        while True:
            print("\nAdd an AI application:")
            name = input("App name (or press Enter to finish): ").strip()
            if not name:
                break
                
            shortcut = input("Shortcut path: ").strip()
            if not shortcut:
                continue
                
            keywords = input("Keywords (comma-separated): ").strip()
            if not keywords:
                keywords = name.lower()
            
            priority = input("Priority (0-10, lower is higher priority): ").strip()
            try:
                priority = int(priority)
            except:
                priority = 999
            
            ai_app = {
                'name': name,
                'shortcut': shortcut,
                'keywords': [k.strip().lower() for k in keywords.split(',')],
                'enabled': True,
                'selected': True,
                'priority': priority
            }
            
            ai_apps.append(ai_app)
            print(f"Added {name}")
        
        config['ai_apps'] = ai_apps
    
    # Additional configuration options
    print("\nAdditional Configuration:")
    
    # Grid layout
    try:
        cols = int(input(f"Grid columns (current: {config['window']['grid']['cols']}): ") or config['window']['grid']['cols'])
        rows = int(input(f"Grid rows (current: {config['window']['grid']['rows']}): ") or config['window']['grid']['rows'])
        config['window']['grid']['cols'] = cols
        config['window']['grid']['rows'] = rows
    except ValueError:
        print("Using default grid layout")
    
    # Display preference
    try:
        display = int(input(f"Preferred display (current: {config['window']['display']['preferred_display']}): ") or config['window']['display']['preferred_display'])
        config['window']['display']['preferred_display'] = display
    except ValueError:
        print("Using default display preference")
    
    # Save configuration
    if save_config(config):
        print("\nConfiguration saved to src/multi_ai_chat/config/config.yml")
        print("\nSetup complete! You can now run Multi-AI Chat Manager")
        
        # Display summary
        ai_count = len(config.get('ai_apps', []))
        if ai_count > 0:
            print(f"\nSummary:")
            print(f"  • {ai_count} AI applications configured")
            print(f"  • Grid layout: {config['window']['grid']['cols']}x{config['window']['grid']['rows']}")
            print(f"  • Display: {config['window']['display']['preferred_display']}")
            
            print(f"\nConfigured AI Apps:")
            for app in sorted(config['ai_apps'], key=lambda x: x['priority']):
                status = "Enabled" if app['enabled'] else "Disabled"
                selected = "Selected" if app.get('selected', True) else "Not Selected"
                print(f"  • {app['name']}: {status}, {selected}, Priority: {app['priority']}")
                print(f"    Shortcut: {app['shortcut']}")
        else:
            print("\nNo AI applications configured")
            print("Edit config.yml manually to add your AI application shortcuts")
    else:
        print("\nFailed to save configuration")

def validate_config():
    """Validate existing configuration"""
    config_path = "src/multi_ai_chat/config/config.yml"
    
    if not os.path.exists(config_path):
        print("No configuration file found")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("Configuration validation:")
        
        # Check required sections
        required_sections = ['app', 'window', 'ai_apps', 'gui', 'history']
        for section in required_sections:
            if section in config:
                print(f"  • {section}: OK")
            else:
                print(f"  • {section}: Missing")
        
        # Check AI apps
        ai_apps = config.get('ai_apps', [])
        print(f"  • AI applications: {len(ai_apps)} configured")
        
        for app in ai_apps:
            shortcut_path = app.get('shortcut', '')
            if os.path.exists(shortcut_path):
                print(f"    • {app['name']}: Shortcut exists")
            else:
                print(f"    • {app['name']}: Shortcut not found - {shortcut_path}")
        
        return True
        
    except Exception as e:
        print(f"Error validating configuration: {e}")
        return False

def main():
    """Main function"""
    try:
        print("Multi-AI Chat Manager v1.0.0 - Configuration Helper")
        print("1. Interactive Setup")
        print("2. Validate Existing Configuration")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            interactive_setup()
        elif choice == '2':
            validate_config()
        elif choice == '3':
            print("Exiting...")
            return
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
    except Exception as e:
        print(f"\nError during setup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()