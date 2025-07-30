#!/usr/bin/env python3
"""
Configuration Helper for Multi-AI Chat Manager
Helps users easily configure their AI application shortcuts
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
    path_lower = path.lower()
    
    if any(keyword in name_lower for keyword in ['chatgpt', 'chat gpt', 'openai']):
        return {
            'name': 'ChatGPT',
            'keywords': ['chatgpt', 'chat.openai', 'openai']
        }
    elif any(keyword in name_lower for keyword in ['claude', 'anthropic']):
        return {
            'name': 'Claude',
            'keywords': ['claude', 'anthropic']
        }
    elif any(keyword in name_lower for keyword in ['gemini', 'bard']):
        return {
            'name': 'Google Gemini',
            'keywords': ['gemini', 'bard', 'google']
        }
    elif 'perplexity' in name_lower:
        return {
            'name': 'Perplexity',
            'keywords': ['perplexity']
        }
    elif any(keyword in name_lower for keyword in ['grok', 'x.ai']):
        return {
            'name': 'Grok',
            'keywords': ['grok', 'x.ai']
        }
    elif 'deepseek' in name_lower:
        return {
            'name': 'DeepSeek',
            'keywords': ['deepseek']
        }
    elif any(keyword in name_lower for keyword in ['copilot', 'bing']):
        return {
            'name': 'Microsoft Copilot',
            'keywords': ['copilot', 'bing']
        }
    else:
        return {
            'name': name,
            'keywords': [name_lower.replace(' ', '')]
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
            'enabled': True
        }
        
        ai_apps.append(ai_app)
    
    return ai_apps

def load_existing_config():
    """Load existing configuration if it exists"""
    if os.path.exists("config.yml"):
        try:
            with open("config.yml", 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading existing config: {e}")
            return None
    return None

def save_config(config):
    """Save configuration to file"""
    try:
        with open("config.yml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def interactive_setup():
    """Interactive configuration setup"""
    print("🚀 Multi-AI Chat Manager - Configuration Helper")
    print("=" * 50)
    
    # Search for shortcuts
    print("🔍 Searching for AI application shortcuts...")
    shortcuts = find_ai_shortcuts()
    
    if shortcuts:
        print(f"✅ Found {len(shortcuts)} potential AI application shortcuts:")
        for i, shortcut in enumerate(shortcuts, 1):
            print(f"  {i}. {shortcut['name']} -> {shortcut['path']}")
    else:
        print("⚠️ No AI application shortcuts found automatically")
        print("You can manually add them later in config.yml")
    
    # Load or create config
    config = load_existing_config()
    if config:
        print("\n✅ Found existing config.yml")
        update = input("Do you want to update it with found shortcuts? (y/n): ").lower()
        if update != 'y':
            print("Configuration unchanged")
            return
    else:
        print("\n📝 Creating new configuration...")
        config = {
            'app': {
                'name': 'Multi-AI Chat Manager',
                'version': '2.0.0'
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
                    'width': 900,
                    'height': 700,
                    'always_on_top': True,
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
                'history_file': 'input_history.txt'
            }
        }
    
    # Configure AI apps
    if shortcuts:
        print("\n📱 Configuring AI applications...")
        
        selected_shortcuts = []
        for i, shortcut in enumerate(shortcuts, 1):
            use_app = input(f"Include {shortcut['name']}? (y/n): ").lower()
            if use_app == 'y':
                selected_shortcuts.append(shortcut)
        
        if selected_shortcuts:
            config['ai_apps'] = create_ai_app_config(selected_shortcuts)
            print(f"✅ Configured {len(selected_shortcuts)} AI applications")
        else:
            config['ai_apps'] = []
            print("⚠️ No AI applications selected")
    else:
        # Manual configuration
        print("\n✏️ Manual AI application configuration:")
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
            
            ai_app = {
                'name': name,
                'shortcut': shortcut,
                'keywords': [k.strip().lower() for k in keywords.split(',')],
                'enabled': True
            }
            
            ai_apps.append(ai_app)
            print(f"✅ Added {name}")
        
        config['ai_apps'] = ai_apps
    
    # Save configuration
    if save_config(config):
        print("\n✅ Configuration saved to config.yml")
        print("\n🎉 Setup complete! You can now run Multi-AI Chat Manager")
        
        # Display summary
        ai_count = len(config.get('ai_apps', []))
        if ai_count > 0:
            print(f"\n📊 Summary:")
            print(f"  • {ai_count} AI applications configured")
            print(f"  • Grid layout: {config['window']['grid']['cols']}x{config['window']['grid']['rows']}")
            print(f"  • Display: {config['window']['display']['preferred_display']}")
            
            print(f"\n📱 Configured AI Apps:")
            for app in config['ai_apps']:
                status = "✅" if app['enabled'] else "❌"
                print(f"  {status} {app['name']}: {app['shortcut']}")
        else:
            print("\n⚠️ No AI applications configured")
            print("Edit config.yml manually to add your AI application shortcuts")
    else:
        print("\n❌ Failed to save configuration")

def main():
    """Main function"""
    try:
        interactive_setup()
    except KeyboardInterrupt:
        print("\n⚠️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()