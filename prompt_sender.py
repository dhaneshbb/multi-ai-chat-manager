"""
Reliable Prompt Sender for AI Chat Applications
Uses the exact working method from your original code
"""

import time
import win32gui
import win32clipboard
import win32com.client
import logging
from typing import List, Dict

class ReliablePromptSender:
    """
    Initialize the ReliablePromptSender object
    :param config: The application configuration
    """
    def __init__(self, config: Dict):
        """
        Initialize the ReliablePromptSender object
        :param config: The application configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.original_foreground = None  # Store the original foreground window
        
    def send_prompt_to_all(self, windows: List[int], window_info: Dict, prompt: str) -> Dict:
        """Send prompt to all AI windows using proven working method"""
        if not prompt.strip():
            return {'success': 0, 'failed': 0, 'total': 0}
        
        if not windows:
            return {'success': 0, 'failed': 0, 'total': 0}
        
        self.logger.info(f"Sending prompt to {len(windows)} AI applications")
        
        # Store original foreground window
        self.original_foreground = win32gui.GetForegroundWindow()
        
        success_count = 0
        
        # Send to each window using the exact working method
        for i, hwnd in enumerate(windows):
            try:
                window_title = win32gui.GetWindowText(hwnd)
                app_name = window_info.get(hwnd, {}).get('app_name', window_title)
                
                self.logger.debug(f"Sending to {app_name}...")
                
                if self._send_prompt_to_window(hwnd, prompt):
                    success_count += 1
                    self.logger.debug(f"Successfully sent to {app_name}")
                
                # Wait between sends (from your original code)
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error with window {i+1}: {e}")
                continue
        
        # Restore original foreground window
        self._restore_original_focus()
        
        failed_count = len(windows) - success_count
        
        self.logger.info(f"Prompt sent to {success_count}/{len(windows)} applications")
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': len(windows)
        }
    
    def _send_prompt_to_window(self, hwnd: int, prompt: str) -> bool:
        """Send prompt to a specific window - exact method from your working code"""
        try:
            # Bring window to foreground
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            
            # Copy prompt to clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(prompt)
            win32clipboard.CloseClipboard()
            
            # Simulate Ctrl+V to paste
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("^v")  # Ctrl+V
            time.sleep(0.1)
            shell.SendKeys("{ENTER}")  # Enter
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending prompt: {e}")
            return False
    
    def _restore_original_focus(self):
        """Restore focus to original window"""
        try:
            if self.original_foreground and win32gui.IsWindow(self.original_foreground):
                win32gui.SetForegroundWindow(self.original_foreground)
                self.logger.debug("Restored original window focus")
        except Exception as e:
            self.logger.debug(f"Could not restore original focus: {e}")