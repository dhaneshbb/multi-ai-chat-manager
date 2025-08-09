#!/usr/bin/env python3
"""
Multi-AI Chat Manager v1.0.0 - Main Application
 AI chat management tool with selective AI targeting
"""

import os
import sys
import logging
import threading
import time
from pathlib import Path

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "multi_ai_chat.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Multi-AI Chat Manager v1.0.0 started")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Executable: {sys.executable}")
    
    return logger

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import yaml
        import win32gui
        import win32clipboard
        import win32com.client
        import psutil
        import tkinter
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install: pip install PyYAML psutil pywin32")
        return False

def load_configuration():
    """Load configuration from external config.yml files only"""
    config_files = [
        "config.yml",  # Root directory
        "src/multi_ai_chat/config/config.yml",  # Development structure
        "config/config.yml",  # Alternative location
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.yml"),  # Relative to main.py
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yml"),  # Up from src structure
    ]
    
    for config_path in config_files:
        if os.path.exists(config_path):
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                print(f"Configuration loaded from: {config_path}")
                return config
            except Exception as e:
                print(f"Error loading config from {config_path}: {e}")
                continue
    
    print("ERROR: No config.yml found!")
    print("Please create a config.yml file or run: python scripts/setup_config.py")
    print("Expected locations:")
    for path in config_files:
        print(f"  - {os.path.abspath(path)}")
    return None

def main():
    """Main application entry point"""
    try:
        print("Multi-AI Chat Manager v1.0.0")
        print("=" * 40)
        
        # Setup logging
        logger = setup_logging()
        
        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            return
        
        # Load configuration - external only
        config = load_configuration()
        if not config:
            print("\nConfiguration is required to run the application.")
            print("Please create config.yml or run the setup wizard:")
            print("  python scripts/setup_config.py")
            input("\nPress Enter to exit...")
            return
        
        print("Configuration loaded successfully")
        
        # Validate required sections
        required_sections = ['app', 'window', 'ai_apps', 'gui', 'history']
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            print(f"\nERROR: Missing required configuration sections: {missing_sections}")
            print("Please check your config.yml file or run the setup wizard:")
            print("  python scripts/setup_config.py")
            input("\nPress Enter to exit...")
            return
        
        # Import modules after dependency check
        try:
            from gui.window_manager import WindowManager
            from core.prompt_sender import ReliablePromptSender
            from gui.interface import CleanGUI
            from core.input_history import InputHistoryManager
            
            print("All modules imported successfully")
        except ImportError as e:
            logger.error(f"Failed to import modules: {e}")
            print(f"Failed to import modules: {e}")
            input("Press Enter to exit...")
            return
        
        # Initialize components
        window_manager = WindowManager(config)
        prompt_sender = ReliablePromptSender(config)
        history_manager = InputHistoryManager(config)
        
        logger.info("All components initialized")
        
        # Define callback functions
        def send_prompt_callback(prompt, selected_apps):
            """Send prompt to selected AI applications"""
            try:
                if not window_manager.ai_windows:
                    logger.warning("No AI windows available for prompt sending")
                    return {'success': 0, 'failed': 0, 'total': 0}
                
                # Filter windows by selected apps
                selected_windows = []
                for hwnd in window_manager.ai_windows:
                    window_info = window_manager.window_info.get(hwnd, {})
                    app_name = window_info.get('app_name', '')
                    if app_name in selected_apps:
                        selected_windows.append(hwnd)
                
                if not selected_windows:
                    logger.warning("No selected AI windows available")
                    return {'success': 0, 'failed': 0, 'total': 0}
                
                result = prompt_sender.send_prompt_to_all(
                    selected_windows,
                    window_manager.window_info,
                    prompt
                )
                
                logger.info(f"Prompt sent: {result['success']}/{result['total']} success")
                return result
                
            except Exception as e:
                logger.error(f"Error sending prompt: {e}")
                return {'success': 0, 'failed': 0, 'total': 0}
        
        def minimize_all_callback():
            """Minimize all AI applications"""
            try:
                result = window_manager.minimize_all_windows()
                logger.info(f"Minimized {result} applications")
                return result
            except Exception as e:
                logger.error(f"Error minimizing apps: {e}")
                return 0
        
        def restore_all_callback():
            """Restore all minimized AI applications"""
            try:
                result = window_manager.restore_all_windows()
                logger.info(f"Restored {result} applications")
                return result
            except Exception as e:
                logger.error(f"Error restoring apps: {e}")
                return 0
        
        def arrange_windows_callback():
            """Arrange windows in grid position"""
            try:
                detected_count = window_manager.refresh_window_list()
                
                if detected_count > 0:
                    display = window_manager.detect_displays()
                    window_manager.arrange_windows_grid(display)
                    logger.info(f"Arranged {detected_count} windows in grid position")
                else:
                    logger.warning("No AI windows found to arrange")
            except Exception as e:
                logger.error(f"Error arranging windows: {e}")
        
        def refresh_windows_callback():
            """Refresh window list"""
            try:
                return window_manager.refresh_window_list()
            except Exception as e:
                logger.error(f"Error refreshing windows: {e}")
                return 0
        
        def bring_to_front_callback(app_name):
            """Bring specific app to front"""
            try:
                result = window_manager.bring_window_to_front(app_name)
                logger.info(f"Brought {app_name} to front: {result}")
                return result
            except Exception as e:
                logger.error(f"Error bringing {app_name} to front: {e}")
                return False
        
        def get_active_apps_callback():
            """Get list of active AI applications"""
            try:
                return window_manager.get_active_apps()
            except Exception as e:
                logger.error(f"Error getting active apps: {e}")
                return []
        
        def reopen_all_callback():
            """Reopen all AI applications"""
            try:
                logger.info("Reopening all applications")
                
                closed_count = window_manager.close_all_windows()
                logger.info(f"Closed {closed_count} windows")
                
                time.sleep(2)
                
                window_manager.launch_apps_parallel()
                time.sleep(3)
                
                window_manager.get_ai_windows_fast()
                display = window_manager.detect_displays()
                window_manager.arrange_windows_grid(display)
                
                detected_count = len(window_manager.ai_windows)
                logger.info(f"Reopened {detected_count} applications")
                
                return detected_count
                
            except Exception as e:
                logger.error(f"Error reopening apps: {e}")
                return 0
        
        def close_all_callback():
            """Close all AI applications"""
            try:
                result = window_manager.close_all_windows()
                logger.info(f"Closed {result} applications")
                return result
            except Exception as e:
                logger.error(f"Error closing apps: {e}")
                return 0
        
        # Create GUI callbacks
        gui_callbacks = {
            'send_prompt': send_prompt_callback,
            'minimize_all': minimize_all_callback,
            'restore_all': restore_all_callback,
            'arrange_windows': arrange_windows_callback,
            'refresh_windows': refresh_windows_callback,
            'bring_to_front': bring_to_front_callback,
            'get_active_apps': get_active_apps_callback,
            'reopen_all': reopen_all_callback,
            'close_all': close_all_callback
        }
        
        # Create and setup GUI
        gui = CleanGUI(config, gui_callbacks)
        gui.set_history_manager(history_manager)
        gui.create_gui()
        
        print("GUI created successfully")
        
        # Initialize AI apps in background
        def init_ai_apps():
            try:
                time.sleep(1)
                
                print("Initializing AI applications")
                
                enabled_apps = [app for app in config['ai_apps'] if app.get('enabled', True)]
                if not enabled_apps:
                    logger.warning("No AI applications configured")
                    gui.update_status("No AI apps configured - edit config.yml", "warning")
                    return
                
                display = window_manager.detect_displays()
                
                window_manager.launch_apps_parallel()
                time.sleep(3)
                
                window_manager.get_ai_windows_fast()
                
                if window_manager.ai_windows:
                    window_manager.arrange_windows_grid(display)
                
                window_count = len(window_manager.ai_windows)
                gui.update_window_count(window_count)
                
                if window_count > 0:
                    gui.update_status(f"Ready! {window_count} AI apps initialized", "success")
                    print(f"{window_count} AI applications ready")
                else:
                    gui.update_status("No AI windows detected - check shortcuts in config.yml", "warning")
                    print("No AI windows detected - check your shortcut paths in config.yml")
                
            except Exception as e:
                logger.error(f"Error initializing AI apps: {e}")
                gui.update_status("Error initializing AI apps", "error")
        
        # Start initialization in background
        threading.Thread(target=init_ai_apps, daemon=True).start()
        
        print("Starting Multi-AI Chat Manager v1.0.0")
        
        # Start GUI main loop
        gui.run()
        
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            logger.error(f"Fatal error: {e}")
            logger.error(traceback.format_exc())
        except:
            pass
    finally:
        print("Multi-AI Chat Manager stopped")

if __name__ == "__main__":
    main()