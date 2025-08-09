'''
Multi-AI Chat Manager v1.0.0 - Prompt Sender
 prompt distribution to selected AI applications
'''

import time
import win32gui
import win32clipboard
import win32com.client
import logging
from typing import List, Dict

class ReliablePromptSender:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.original_foreground = None
        
    def send_prompt_to_all(self, windows: List[int], window_info: Dict, prompt: str) -> Dict:
        """Send prompt to selected AI windows using proven working method"""
        if not prompt.strip():
            return {'success': 0, 'failed': 0, 'total': 0}
        
        if not windows:
            return {'success': 0, 'failed': 0, 'total': 0}
        
        self.logger.info(f"Sending prompt to {len(windows)} selected AI applications")
        
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
                
                # Wait between sends (configurable delay)
                delay = self.config.get('window', {}).get('timing', {}).get('prompt_send_delay', 0.1)
                time.sleep(max(delay, 0.5))  # Minimum 0.5s delay for reliability
                
            except Exception as e:
                self.logger.error(f"Error with window {i+1}: {e}")
                continue
        
        # Restore original foreground window
        self._restore_original_focus()
        
        failed_count = len(windows) - success_count
        
        self.logger.info(f"Prompt sent to {success_count}/{len(windows)} selected applications")
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': len(windows)
        }
    
    def _send_prompt_to_window(self, hwnd: int, prompt: str) -> bool:
        """Send prompt to a specific window - with Unicode clipboard support"""
        try:
            # Ensure window is visible and ready
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32gui.SW_RESTORE)
                time.sleep(0.2)
            
            # Bring window to foreground
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.2)  # Increased delay for stability
            
            # Copy prompt to clipboard with Unicode support
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            # FIX: Use CF_UNICODETEXT format to handle Unicode characters
            win32clipboard.SetClipboardText(prompt, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            # Simulate Ctrl+V to paste
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("^v")  # Ctrl+V
            time.sleep(0.2)  # Wait for paste to complete
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
    
    def send_prompt_to_single(self, hwnd: int, window_info: Dict, prompt: str) -> bool:
        """Send prompt to a single AI window"""
        if not prompt.strip():
            return False
        
        try:
            app_name = window_info.get(hwnd, {}).get('app_name', 'Unknown')
            self.logger.info(f"Sending prompt to {app_name}")
            
            # Store original foreground window
            self.original_foreground = win32gui.GetForegroundWindow()
            
            # Send prompt
            success = self._send_prompt_to_window(hwnd, prompt)
            
            # Restore original focus
            self._restore_original_focus()
            
            if success:
                self.logger.info(f"Successfully sent prompt to {app_name}")
            else:
                self.logger.warning(f"Failed to send prompt to {app_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending prompt to single window: {e}")
            return False
    
    def test_clipboard_functionality(self) -> bool:
        """Test if clipboard operations work properly - with Unicode support"""
        try:
            test_text = "Multi-AI Chat Manager Test with Unicode: éñ中文🤖"
            
            # Test clipboard write with Unicode
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(test_text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            # Test clipboard read
            win32clipboard.OpenClipboard()
            clipboard_content = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            success = clipboard_content == test_text
            
            if success:
                self.logger.info("Unicode clipboard functionality test passed")
            else:
                self.logger.error("Unicode clipboard functionality test failed")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Clipboard test failed: {e}")
            return False
    
    def test_com_automation(self) -> bool:
        """Test if COM automation (WScript.Shell) works properly"""
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Simple test - this should not cause any visible effect
            shell.SendKeys("")
            
            self.logger.info("COM automation test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"COM automation test failed: {e}")
            return False
    
    def get_configuration_info(self) -> Dict:
        """Get current configuration information for diagnostics"""
        return {
            'prompt_send_delay': self.config.get('window', {}).get('timing', {}).get('prompt_send_delay', 0.1),
            'action_delay': self.config.get('window', {}).get('timing', {}).get('action_delay', 0.1),
            'clipboard_test': self.test_clipboard_functionality(),
            'com_automation_test': self.test_com_automation()
        }
