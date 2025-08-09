"""
Multi-AI Chat Manager v1.0.0 - Window Manager
 window management for AI applications
"""

import os
import time
import win32gui
import win32con
import win32api
import win32process
import psutil
import logging
from typing import List, Dict

class WindowManager:
    def __init__(self, config: Dict):
        self.config = config
        self.ai_windows = []
        self.window_info = {}
        self.logger = logging.getLogger(__name__)
        
        # Custom app ordering for grid arrangement
        self.app_priority = {
            'Claude': 0,
            'Google Gemini': 1, 
            'Perplexity': 2,
            'Grok': 3,
            'DeepSeek': 4,
            'ChatGPT': 5
        }
        
    def detect_displays(self) -> Dict:
        """Detect displays and return the configured one"""
        try:
            monitors = win32api.EnumDisplayMonitors()
            displays = []
            
            for i, monitor in enumerate(monitors):
                monitor_info = win32api.GetMonitorInfo(monitor[0])
                work_area = monitor_info['Work']
                
                display_info = {
                    'index': i + 1,
                    'left': work_area[0],
                    'top': work_area[1],
                    'right': work_area[2],
                    'bottom': work_area[3],
                    'width': work_area[2] - work_area[0],
                    'height': work_area[3] - work_area[1],
                    'is_primary': monitor_info.get('Flags', 0) & 1 == 1
                }
                displays.append(display_info)
            
            # Select display based on config
            preferred = self.config['window']['display']['preferred_display']
            if 1 <= preferred <= len(displays):
                selected = displays[preferred - 1]
            else:
                selected = displays[0] if displays else {
                    'left': 0, 'top': 0, 'width': 1920, 'height': 1080
                }
            
            self.logger.info(f"Using display {selected.get('index', 1)}: {selected['width']}x{selected['height']}")
            return selected
            
        except Exception as e:
            self.logger.error(f"Display detection error: {e}")
            return {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
    
    def launch_apps_parallel(self) -> None:
        """Launch all AI applications"""
        enabled_apps = [app for app in self.config['ai_apps'] if app.get('enabled', True)]
        launch_delay = self.config['window']['timing']['launch_delay']
        
        self.logger.info(f"Launching {len(enabled_apps)} AI applications")
        
        launched_count = 0
        for app in enabled_apps:
            try:
                shortcut_path = app['shortcut']
                if os.path.exists(shortcut_path):
                    self.logger.info(f"Launching {app['name']}")
                    os.startfile(shortcut_path)
                    launched_count += 1
                    time.sleep(launch_delay)
                else:
                    self.logger.warning(f"Shortcut not found: {shortcut_path}")
            except Exception as e:
                self.logger.error(f"Error launching {app['name']}: {e}")
        
        self.logger.info(f"Launched {launched_count}/{len(enabled_apps)} applications")
        
        # Wait for apps to load
        load_wait = self.config['window']['timing']['load_wait']
        self.logger.info(f"Waiting {load_wait}s for applications to load")
        time.sleep(load_wait)
    
    def get_ai_windows_fast(self) -> List[int]:
        """Detect AI application windows - includes minimized windows"""
        windows = []
        self.window_info.clear()
        
        # Build keyword mapping
        app_keyword_map = {}
        for app in self.config['ai_apps']:
            if app.get('enabled', True):
                app_keyword_map[app['name']] = [kw.lower() for kw in app['keywords']]
        
        def enum_windows_proc(hwnd, lParam):
            try:
                # Don't filter by visibility - include minimized windows
                window_title = win32gui.GetWindowText(hwnd)
                if not window_title:
                    return True
                
                title_lower = window_title.lower()
                
                for app_name, keywords in app_keyword_map.items():
                    for keyword in keywords:
                        if keyword in title_lower:
                            if self._is_valid_ai_window(hwnd, window_title):
                                windows.append(hwnd)
                                self.window_info[hwnd] = {
                                    'title': window_title,
                                    'app_name': app_name,
                                    'hwnd': hwnd,
                                    'priority': self.app_priority.get(app_name, 999)
                                }
                                self.logger.debug(f"Found {app_name}: {window_title}")
                                
                                # Hide from taskbar after detection
                                self._hide_from_taskbar(hwnd, app_name)
                            return True
                        
            except Exception as e:
                self.logger.debug(f"Window enumeration error: {e}")
            
            return True
        
        win32gui.EnumWindows(enum_windows_proc, None)
        
        self.ai_windows = windows
        self.logger.info(f"Detected {len(self.ai_windows)} AI application windows")
        
        return self.ai_windows
    
    def _hide_from_taskbar(self, hwnd: int, app_name: str) -> None:
        """Hide window from taskbar"""
        try:
            # Set window as tool window (removes from taskbar)
            current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_style = current_style | win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
            
            self.logger.debug(f"Hidden {app_name} from taskbar")
            
        except Exception as e:
            self.logger.debug(f"Could not hide {app_name} from taskbar: {e}")
    
    def _show_in_taskbar(self, hwnd: int, app_name: str) -> None:
        """Show window in taskbar"""
        try:
            # Remove tool window style to show in taskbar
            current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_style = current_style & ~win32con.WS_EX_TOOLWINDOW
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
            
            self.logger.debug(f"Restored {app_name} to taskbar")
            
        except Exception as e:
            self.logger.debug(f"Could not restore {app_name} to taskbar: {e}")
    
    def _is_valid_ai_window(self, hwnd: int, title: str) -> bool:
        """Validate if window is a real AI application"""
        try:
            # Check if window exists
            if not win32gui.IsWindow(hwnd):
                return False
            
            # Check if it's a browser/electron app
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                exe_name = process.name().lower()
                
                valid_executables = [
                    'chrome.exe', 'firefox.exe', 'edge.exe', 'msedge.exe',
                    'brave.exe', 'electron.exe', 'opera.exe'
                ]
                
                return any(exe in exe_name for exe in valid_executables)
            except:
                return True
                
        except Exception:
            return True
    
    def _is_window_maximized(self, hwnd: int) -> bool:
        """Check if window is maximized using placement info"""
        try:
            placement = win32gui.GetWindowPlacement(hwnd)
            return placement[1] == win32con.SW_SHOWMAXIMIZED
        except:
            return False
    
    def arrange_windows_grid(self, display: Dict) -> None:
        """Arrange windows in custom ordered grid"""
        if not self.ai_windows:
            self.logger.warning("No windows to arrange")
            return
        
        grid_cols = self.config['window']['grid']['cols']
        grid_rows = self.config['window']['grid']['rows']
        
        # Sort windows by priority for custom ordering
        sorted_windows = sorted(
            self.ai_windows,
            key=lambda hwnd: self.window_info.get(hwnd, {}).get('priority', 999)
        )
        
        # Calculate window dimensions with padding
        padding = 10
        window_width = (display['width'] - (grid_cols + 1) * padding) // grid_cols
        window_height = (display['height'] - (grid_rows + 1) * padding) // grid_rows
        
        self.logger.info(f"Arranging {len(sorted_windows)} windows in {grid_cols}x{grid_rows} grid")
        self.logger.info(f"Display: {display['width']}x{display['height']} at ({display['left']}, {display['top']})")
        self.logger.info(f"Window size: {window_width}x{window_height} with {padding}px padding")
        
        arranged_count = 0
        for i, hwnd in enumerate(sorted_windows):
            if i >= grid_cols * grid_rows:
                self.logger.warning(f"Too many windows ({len(sorted_windows)}) for {grid_cols}x{grid_rows} grid")
                break
                
            try:
                # Calculate grid position
                col = i % grid_cols
                row = i // grid_cols
                
                # Calculate window position with padding
                x = display['left'] + padding + (col * (window_width + padding))
                y = display['top'] + padding + (row * (window_height + padding))
                
                # Get window info for logging
                window_info = self.window_info.get(hwnd, {})
                app_name = window_info.get('app_name', 'Unknown')
                priority = window_info.get('priority', 999)
                
                self.logger.info(f"Moving {app_name} (priority {priority}) to grid position [{row},{col}] at ({x}, {y})")
                
                # Use improved window arrangement method
                if self._arrange_single_window_improved(hwnd, x, y, window_width, window_height, app_name):
                    arranged_count += 1
                    self.logger.info(f"Successfully arranged {app_name}")
                else:
                    self.logger.warning(f"Failed to arrange {app_name}")
                
                # Small delay between operations
                time.sleep(0.2)
                
            except Exception as e:
                self.logger.error(f"Error arranging window {i} ({app_name}): {e}")
        
        self.logger.info(f"Successfully arranged {arranged_count}/{len(sorted_windows)} windows in grid")
        
        # Verification step
        time.sleep(0.5)
        self._verify_arrangement()
    
    def _arrange_single_window_improved(self, hwnd: int, x: int, y: int, width: int, height: int, app_name: str) -> bool:
        """Improved single window arrangement with better error handling"""
        if not win32gui.IsWindow(hwnd):
            self.logger.warning(f"Window {app_name} no longer exists")
            return False
        
        try:
            self.logger.debug(f"Starting arrangement for {app_name}")
            
            # Step 1: Show window if hidden or minimized
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                time.sleep(0.2)
                
                # Restore if minimized
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)
                
                # Restore if maximized
                if self._is_window_maximized(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)
                    
                self.logger.debug(f"{app_name} window state normalized")
                
            except Exception as e:
                self.logger.debug(f"Error normalizing {app_name} window state: {e}")
            
            # Step 2: Force window to normal state
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
                time.sleep(0.2)
            except Exception as e:
                self.logger.debug(f"Error showing {app_name} normal: {e}")
            
            # Step 3: Try different positioning methods
            success = False
            
            # Method 1: Direct positioning
            try:
                result = win32gui.SetWindowPos(
                    hwnd, 
                    win32con.HWND_TOP,
                    x, y, width, height,
                    win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE
                )
                
                if result:
                    time.sleep(0.2)
                    # Verify position
                    rect = win32gui.GetWindowRect(hwnd)
                    if abs(rect[0] - x) <= 50 and abs(rect[1] - y) <= 50:
                        self.logger.debug(f"{app_name} positioned successfully with method 1")
                        success = True
                    else:
                        self.logger.debug(f"{app_name} method 1 position mismatch: expected ({x},{y}), got ({rect[0]},{rect[1]})")
                        
            except Exception as e:
                self.logger.debug(f"{app_name} method 1 failed: {e}")
            
            # Method 2: Move first, then resize
            if not success:
                try:
                    # Move window
                    move_result = win32gui.SetWindowPos(
                        hwnd, win32con.HWND_TOP, x, y, 0, 0,
                        win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE
                    )
                    
                    time.sleep(0.1)
                    
                    # Resize window
                    if move_result:
                        resize_result = win32gui.SetWindowPos(
                            hwnd, 0, 0, 0, width, height,
                            win32con.SWP_NOMOVE | win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE
                        )
                        
                        if resize_result:
                            time.sleep(0.2)
                            rect = win32gui.GetWindowRect(hwnd)
                            if abs(rect[0] - x) <= 50 and abs(rect[1] - y) <= 50:
                                self.logger.debug(f"{app_name} positioned successfully with method 2")
                                success = True
                            else:
                                self.logger.debug(f"{app_name} method 2 position mismatch")
                                
                except Exception as e:
                    self.logger.debug(f"{app_name} method 2 failed: {e}")
            
            # Method 3: Use MoveWindow as fallback
            if not success:
                try:
                    result = win32gui.MoveWindow(hwnd, x, y, width, height, True)
                    if result:
                        time.sleep(0.2)
                        rect = win32gui.GetWindowRect(hwnd)
                        if abs(rect[0] - x) <= 50 and abs(rect[1] - y) <= 50:
                            self.logger.debug(f"{app_name} positioned successfully with method 3")
                            success = True
                        else:
                            self.logger.debug(f"{app_name} method 3 position mismatch")
                            
                except Exception as e:
                    self.logger.debug(f"{app_name} method 3 failed: {e}")
            
            if success:
                # Final verification and adjustment
                try:
                    win32gui.UpdateWindow(hwnd)
                    self.logger.debug(f"{app_name} window updated")
                except:
                    pass
                    
                return True
            else:
                self.logger.warning(f"All positioning methods failed for {app_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Critical error arranging {app_name}: {e}")
            return False
    
    def bring_window_to_front(self, app_name: str) -> bool:
        """Bring specific AI app window to front"""
        for hwnd in self.ai_windows:
            window_info = self.window_info.get(hwnd, {})
            if window_info.get('app_name') == app_name:
                try:
                    # First ensure window is not minimized
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        time.sleep(0.2)
                    
                    # Show window
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    time.sleep(0.1)
                    
                    # Bring to front
                    win32gui.SetForegroundWindow(hwnd)
                    win32gui.BringWindowToTop(hwnd)
                    
                    self.logger.info(f"Brought {app_name} to front")
                    return True
                    
                except Exception as e:
                    self.logger.error(f"Error bringing {app_name} to front: {e}")
                    return False
        
        self.logger.warning(f"Window for {app_name} not found")
        return False
    
    def minimize_all_windows(self) -> int:
        """Minimize all AI application windows"""
        minimized_count = 0
        
        for hwnd in self.ai_windows:
            try:
                if win32gui.IsWindow(hwnd):
                    # Only minimize if not already minimized
                    if not win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                        minimized_count += 1
                        time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error minimizing window: {e}")
        
        self.logger.info(f"Minimized {minimized_count} windows")
        return minimized_count
    
    def restore_all_windows(self) -> int:
        """Restore all minimized AI windows"""
        restored_count = 0
        
        for hwnd in self.ai_windows:
            try:
                if win32gui.IsWindow(hwnd):
                    # Restore if minimized
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        restored_count += 1
                        time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error restoring window: {e}")
        
        self.logger.info(f"Restored {restored_count} windows")
        return restored_count
    
    def restore_taskbar_icons(self) -> int:
        """Restore AI applications to taskbar when closing"""
        restored_count = 0
        
        for hwnd in self.ai_windows:
            try:
                if win32gui.IsWindow(hwnd):
                    app_name = self.window_info.get(hwnd, {}).get('app_name', 'Unknown')
                    self._show_in_taskbar(hwnd, app_name)
                    restored_count += 1
            except Exception as e:
                self.logger.error(f"Error restoring taskbar icon: {e}")
        
        self.logger.info(f"Restored {restored_count} taskbar icons")
        return restored_count
    
    def get_active_apps(self) -> List[Dict]:
        """Get list of active AI applications for GUI display"""
        active_apps = []
        
        for hwnd in self.ai_windows:
            try:
                if win32gui.IsWindow(hwnd):
                    window_info = self.window_info.get(hwnd, {})
                    app_name = window_info.get('app_name', 'Unknown')
                    
                    active_apps.append({
                        'name': app_name,
                        'hwnd': hwnd,
                        'title': window_info.get('title', ''),
                        'priority': window_info.get('priority', 999),
                        'is_minimized': win32gui.IsIconic(hwnd)
                    })
            except Exception as e:
                self.logger.debug(f"Error getting app info: {e}")
        
        # Sort by priority
        active_apps.sort(key=lambda x: x['priority'])
        return active_apps
    
    def _verify_arrangement(self) -> None:
        """Verify that windows are correctly positioned"""
        verification_count = 0
        for i, hwnd in enumerate(self.ai_windows):
            try:
                if win32gui.IsWindow(hwnd):
                    rect = win32gui.GetWindowRect(hwnd)
                    app_name = self.window_info.get(hwnd, {}).get('app_name', 'Unknown')
                    is_minimized = win32gui.IsIconic(hwnd)
                    self.logger.debug(f"{app_name} final position: ({rect[0]}, {rect[1]}) size: {rect[2]-rect[0]}x{rect[3]-rect[1]} minimized: {is_minimized}")
                    verification_count += 1
            except Exception as e:
                self.logger.debug(f"Verification error for window: {e}")
        
        self.logger.info(f"Verified {verification_count} windows are positioned correctly")
    
    def refresh_window_list(self) -> int:
        """Refresh the list of AI windows"""
        old_count = len(self.ai_windows)
        self.get_ai_windows_fast()
        new_count = len(self.ai_windows)
        
        self.logger.info(f"Window list refreshed: {old_count} -> {new_count} windows")
        return new_count
    
    def close_all_windows(self) -> int:
        """Close all AI application windows"""
        # First restore taskbar icons
        self.restore_taskbar_icons()
        
        closed_count = 0
        
        for hwnd in self.ai_windows:
            try:
                if win32gui.IsWindow(hwnd):
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    closed_count += 1
            except Exception as e:
                self.logger.error(f"Error closing window: {e}")
        
        self.ai_windows.clear()
        self.window_info.clear()
        
        self.logger.info(f"Closed {closed_count} windows")
        return closed_count