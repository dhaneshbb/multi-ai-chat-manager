"""
Multi-AI Chat Manager v1.0.0 - GUI Interface
 interface with AI selection capabilities
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import logging
from typing import Dict, Callable, List

class CleanGUI:
    def __init__(self, config: Dict, callbacks: Dict[str, Callable]):
        self.config = config
        self.callbacks = callbacks
        self.logger = logging.getLogger(__name__)
        
        # GUI components
        self.root = None
        self.prompt_text = None
        self.status_label = None
        self.window_count_label = None
        self.app_icons_frame = None
        self.app_selection_frame = None
        self.app_buttons = {}
        self.ai_selection_vars = {}
        
        # State
        self.history_manager = None
        self.active_apps = []
        
        # Colors
        self.colors = config['gui']['theme']
        
    def set_history_manager(self, history_manager):
        """Set the history manager"""
        self.history_manager = history_manager
        
    def create_gui(self):
        """Create the main GUI"""
        self.root = tk.Tk()
        self.root.title(self.config['app']['name'])
        
        # Window setup
        gui_config = self.config['gui']['window']
        self.root.geometry(f"{gui_config['width']}x{gui_config['height']}")
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Normal window behavior (removed always_on_top)
        if gui_config.get('resizable', True):
            self.root.resizable(True, True)
        
        # Create interface
        self._create_header()
        self._create_ai_selection_section()
        self._create_app_icons_section()
        self._create_main_content()
        self._create_control_panel()
        self._create_status_bar()
        self._bind_hotkeys()
        
        # Focus input
        self.prompt_text.focus_set()
        
        self.logger.info("GUI created successfully")
    
    def _create_header(self):
        """Create header with title and status"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=50)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=f"{self.config['app']['name']} v{self.config['app']['version']}",
            font=self.config['gui']['fonts']['title'],
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary']
        )
        title_label.pack(side=tk.LEFT, anchor='w')
        
        # Status info
        info_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        info_frame.pack(side=tk.RIGHT, anchor='e')
        
        self.window_count_label = tk.Label(
            info_frame,
            text="No AI apps connected",
            font=self.config['gui']['fonts']['normal'],
            bg=self.colors['bg_primary'],
            fg=self.colors['success_color']
        )
        self.window_count_label.pack(anchor='e')
        
        self.status_label = tk.Label(
            info_frame,
            text="Ready",
            font=self.config['gui']['fonts']['small'],
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_secondary']
        )
        self.status_label.pack(anchor='e')
    
    def _create_ai_selection_section(self):
        """Create AI selection checkboxes section"""
        selection_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        selection_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Section label
        selection_label = tk.Label(
            selection_frame,
            text="Select AI Applications for Prompts:",
            font=self.config['gui']['fonts']['normal'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_primary']
        )
        selection_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # AI selection container
        self.app_selection_frame = tk.Frame(selection_frame, bg=self.colors['bg_secondary'])
        self.app_selection_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        # Control buttons for selection
        control_frame = tk.Frame(selection_frame, bg=self.colors['bg_secondary'])
        control_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        select_all_btn = self._create_button(
            control_frame,
            "Select All",
            self._select_all_ai,
            style='secondary',
            width=10
        )
        select_all_btn.pack(side=tk.LEFT, padx=2)
        
        select_none_btn = self._create_button(
            control_frame,
            "Select None",
            self._select_none_ai,
            style='secondary',
            width=10
        )
        select_none_btn.pack(side=tk.LEFT, padx=2)
    
    def _create_app_icons_section(self):
        """Create section with individual AI app icons"""
        app_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=60)
        app_frame.pack(fill=tk.X, padx=20, pady=5)
        app_frame.pack_propagate(False)
        
        # Section label
        app_label = tk.Label(
            app_frame,
            text="AI Applications Status:",
            font=self.config['gui']['fonts']['normal'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_primary']
        )
        app_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # App icons container
        self.app_icons_frame = tk.Frame(app_frame, bg=self.colors['bg_secondary'])
        self.app_icons_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
    
    def _create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Input section
        prompt_label = tk.Label(
            main_frame,
            text="Enter prompt for selected AI applications:",
            font=self.config['gui']['fonts']['normal'],
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary']
        )
        prompt_label.pack(anchor='w', pady=(0, 5))
        
        # Text input area
        text_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.prompt_text = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            font=self.config['gui']['fonts']['normal'],
            bg=self.colors['bg_input'],
            fg=self.colors['fg_primary'],
            insertbackground=self.colors['fg_primary'],
            selectbackground=self.colors['accent_color'],
            relief='flat',
            bd=5,
            wrap=tk.WORD
        )
        self.prompt_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    def _create_control_panel(self):
        """Create horizontal control buttons"""
        control_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Main control buttons row
        buttons_row = tk.Frame(control_frame, bg=self.colors['bg_primary'])
        buttons_row.pack(fill=tk.X)
        
        # Send button (primary action)
        send_btn = self._create_button(
            buttons_row,
            "Send to Selected AI Apps",
            self._on_send_prompt,
            style='primary',
            width=20
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Window control buttons
        minimize_btn = self._create_button(
            buttons_row,
            "Minimize All",
            self._on_minimize_all,
            style='secondary',
            width=12
        )
        minimize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        maximize_btn = self._create_button(
            buttons_row,
            "Maximize Grid",
            self._on_maximize_grid,
            style='accent',
            width=12
        )
        maximize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Spacer
        spacer = tk.Frame(buttons_row, bg=self.colors['bg_primary'])
        spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Management buttons on the right
        reopen_btn = self._create_button(
            buttons_row,
            "Reopen All",
            self._on_reopen_all,
            style='accent',
            width=12
        )
        reopen_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        close_btn = self._create_button(
            buttons_row,
            "Close All",
            self._on_close_all,
            style='danger',
            width=12
        )
        close_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _create_button(self, parent, text: str, command: Callable, style: str = 'normal', width: int = 12):
        """Create a styled button"""
        colors = {
            'primary': {'bg': self.colors['accent_color'], 'fg': 'white', 'active_bg': '#106ebe'},
            'secondary': {'bg': self.colors['bg_secondary'], 'fg': self.colors['fg_primary'], 'active_bg': '#404040'},
            'accent': {'bg': self.colors['success_color'], 'fg': 'white', 'active_bg': '#45a049'},
            'danger': {'bg': self.colors['error_color'], 'fg': 'white', 'active_bg': '#da190b'},
            'app': {'bg': '#333333', 'fg': 'white', 'active_bg': '#555555'},
            'normal': {'bg': '#666666', 'fg': 'white', 'active_bg': '#777777'}
        }
        
        btn_colors = colors.get(style, colors['normal'])
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.config['gui']['fonts']['button'],
            bg=btn_colors['bg'],
            fg=btn_colors['fg'],
            activebackground=btn_colors['active_bg'],
            activeforeground=btn_colors['fg'],
            relief='flat',
            cursor='hand2',
            width=width,
            pady=4
        )
        
        # Hover effects
        def on_enter(e):
            button.config(bg=btn_colors['active_bg'])
        
        def on_leave(e):
            button.config(bg=btn_colors['bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # Hotkey hints
        hints_text = "Hotkeys: Enter=Send | Shift+Enter=New Line | Select AIs above to target specific models"
        hints_label = tk.Label(
            status_frame,
            text=hints_text,
            font=self.config['gui']['fonts']['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_secondary']
        )
        hints_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        # Version
        version_label = tk.Label(
            status_frame,
            text=f"v{self.config['app']['version']}",
            font=self.config['gui']['fonts']['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_secondary']
        )
        version_label.pack(side=tk.RIGHT, padx=10, pady=3)
    
    def _bind_hotkeys(self):
        """Bind keyboard shortcuts - removed arrow key navigation"""
        self.prompt_text.bind("<Return>", self._on_enter_key)
        self.prompt_text.bind("<Shift-Return>", self._on_shift_enter)
    
    def _on_enter_key(self, event):
        """Handle Enter key"""
        self._on_send_prompt()
        return "break"
    
    def _on_shift_enter(self, event):
        """Handle Shift+Enter for new line"""
        return None
    
    def _select_all_ai(self):
        """Select all AI applications"""
        for var in self.ai_selection_vars.values():
            var.set(True)
    
    def _select_none_ai(self):
        """Deselect all AI applications"""
        for var in self.ai_selection_vars.values():
            var.set(False)
    
    def _get_selected_apps(self):
        """Get list of selected AI applications"""
        selected = []
        for app_name, var in self.ai_selection_vars.items():
            if var.get():
                selected.append(app_name)
        return selected
    
    def _on_send_prompt(self):
        """Handle send prompt action"""
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            self.update_status("Please enter a prompt", "warning")
            return
        
        # Get selected AI applications
        selected_apps = self._get_selected_apps()
        if not selected_apps:
            self.update_status("Please select at least one AI application", "warning")
            return
        
        # Add to history
        if self.history_manager:
            self.history_manager.add_entry(prompt)
        
        selected_count = len(selected_apps)
        self.update_status(f"Sending prompt to {selected_count} selected AI applications", "info")
        
        # Send in background thread
        def send_async():
            try:
                result = self.callbacks['send_prompt'](prompt, selected_apps)
                
                if result['success'] > 0:
                    status_msg = f"Sent to {result['success']}/{result['total']} selected applications"
                    self.update_status(status_msg, "success")
                    
                    # Clear prompt after successful send
                    self.root.after(0, self._clear_prompt_text)
                else:
                    self.update_status("No selected applications received the prompt", "warning")
                    
            except Exception as e:
                self.logger.error(f"Error sending prompt: {e}")
                self.update_status("Error occurred while sending", "error")
        
        threading.Thread(target=send_async, daemon=True).start()
    
    def _clear_prompt_text(self):
        """Clear the prompt text"""
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.focus_set()
    
    def _on_minimize_all(self):
        """Handle minimize all windows"""
        self.update_status("Minimizing all AI applications", "info")
        
        def minimize_async():
            try:
                result = self.callbacks['minimize_all']()
                self.update_status(f"Minimized {result} applications", "success")
                self._update_app_buttons_state()
            except Exception as e:
                self.update_status("Error minimizing apps", "error")
        
        threading.Thread(target=minimize_async, daemon=True).start()
    
    def _on_maximize_grid(self):
        """Handle maximize/arrange windows in grid"""
        self.update_status("Restoring and arranging windows in grid position", "info")
        
        def maximize_async():
            try:
                self.callbacks['refresh_windows']()
                
                if 'restore_all' in self.callbacks:
                    restored = self.callbacks['restore_all']()
                    if restored > 0:
                        self.update_status(f"Restored {restored} minimized windows, arranging in grid", "info")
                        import time
                        time.sleep(0.5)
                
                self.callbacks['arrange_windows']()
                self.update_status("Windows restored and arranged in grid position", "success")
                self._update_app_buttons_state()
                
            except Exception as e:
                self.logger.error(f"Error in maximize grid: {e}")
                self.update_status("Error arranging windows", "error")
        
        threading.Thread(target=maximize_async, daemon=True).start()
    
    def _on_reopen_all(self):
        """Handle reopen all apps"""
        if messagebox.askyesno("Confirm", "Close all AI windows and reopen them?"):
            self.update_status("Reopening all applications", "info")
            
            def reopen_async():
                try:
                    result = self.callbacks['reopen_all']()
                    self.update_status(f"Reopened {result} applications", "success")
                    self._update_app_icons()
                    self._update_ai_selection()
                except Exception as e:
                    self.update_status("Error reopening apps", "error")
            
            threading.Thread(target=reopen_async, daemon=True).start()
    
    def _on_close_all(self):
        """Handle close all apps"""
        if messagebox.askyesno("Confirm", "Close all AI application windows?"):
            try:
                result = self.callbacks['close_all']()
                self.update_status(f"Closed {result} applications", "success")
                self.update_window_count(0)
                self._clear_app_icons()
            except Exception as e:
                self.update_status("Error closing apps", "error")
    
    def _on_app_click(self, app_name: str):
        """Handle clicking on individual app icon"""
        self.update_status(f"Bringing {app_name} to front", "info")
        
        def bring_to_front_async():
            try:
                self.callbacks['refresh_windows']()
                
                success = self.callbacks['bring_to_front'](app_name)
                if success:
                    self.update_status(f"{app_name} brought to front", "success")
                else:
                    self.update_status(f"Could not bring {app_name} to front", "warning")
                
                self._update_app_buttons_state()
            except Exception as e:
                self.update_status(f"Error with {app_name}", "error")
        
        threading.Thread(target=bring_to_front_async, daemon=True).start()
    
    def _create_ai_selection_checkboxes(self):
        """Create AI selection checkboxes"""
        # Clear existing checkboxes
        for widget in self.app_selection_frame.winfo_children():
            widget.destroy()
        self.ai_selection_vars.clear()
        
        # Create checkboxes for each configured AI app
        for app in self.config['ai_apps']:
            if app.get('enabled', True):
                app_name = app['name']
                var = tk.BooleanVar(value=app.get('selected', True))
                self.ai_selection_vars[app_name] = var
                
                checkbox = tk.Checkbutton(
                    self.app_selection_frame,
                    text=app_name,
                    variable=var,
                    font=self.config['gui']['fonts']['small'],
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['fg_primary'],
                    selectcolor=self.colors['bg_input'],
                    activebackground=self.colors['bg_secondary'],
                    activeforeground=self.colors['fg_primary']
                )
                checkbox.pack(side=tk.LEFT, padx=5)
    
    def _create_app_icons(self, apps: List[Dict]):
        """Create clickable app icons"""
        # Clear existing buttons
        self._clear_app_icons()
        
        for app in apps:
            app_name = app['name']
            is_minimized = app.get('is_minimized', False)
            
            # Create button for each app
            app_btn = self._create_button(
                self.app_icons_frame,
                app_name,
                lambda name=app_name: self._on_app_click(name),
                style='app',
                width=len(app_name) + 2
            )
            
            # Visual indicator for minimized state
            if is_minimized:
                app_btn.config(bg='#555555', fg='#cccccc')
            else:
                app_btn.config(bg='#333333', fg='white')
            
            app_btn.pack(side=tk.LEFT, padx=2)
            self.app_buttons[app_name] = app_btn
    
    def _clear_app_icons(self):
        """Clear all app icon buttons"""
        for button in self.app_buttons.values():
            button.destroy()
        self.app_buttons.clear()
    
    def _update_app_icons(self):
        """Update app icons from window manager"""
        if 'get_active_apps' in self.callbacks:
            try:
                self.callbacks['refresh_windows']()
                apps = self.callbacks['get_active_apps']()
                self.active_apps = apps
                self._create_app_icons(apps)
            except Exception as e:
                self.logger.error(f"Error updating app icons: {e}")
    
    def _update_ai_selection(self):
        """Update AI selection checkboxes"""
        self._create_ai_selection_checkboxes()
    
    def _update_app_buttons_state(self):
        """Update the visual state of app buttons"""
        if 'get_active_apps' in self.callbacks:
            try:
                apps = self.callbacks['get_active_apps']()
                
                for app in apps:
                    app_name = app['name']
                    is_minimized = app.get('is_minimized', False)
                    
                    if app_name in self.app_buttons:
                        button = self.app_buttons[app_name]
                        if is_minimized:
                            button.config(bg='#555555', fg='#cccccc')
                        else:
                            button.config(bg='#333333', fg='white')
                            
            except Exception as e:
                self.logger.error(f"Error updating app button states: {e}")
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status label"""
        colors = {
            'info': self.colors['fg_secondary'],
            'success': self.colors['success_color'],
            'warning': self.colors['warning_color'],
            'error': self.colors['error_color']
        }
        
        color = colors.get(status_type, colors['info'])
        
        def update():
            self.status_label.config(text=message, fg=color)
        
        if self.root:
            self.root.after(0, update)
    
    def update_window_count(self, count: int):
        """Update window count and app icons"""
        text = f"{count} AI applications connected" if count > 0 else "No AI apps connected"
        
        def update():
            self.window_count_label.config(text=text)
            if count > 0:
                self._update_app_icons()
                self._update_ai_selection()
            else:
                self._clear_app_icons()
        
        if self.root:
            self.root.after(0, update)
    
    def run(self):
        """Start GUI"""
        if self.root:
            self.root.mainloop()
    
    def destroy(self):
        """Cleanup"""
        if self.root:
            self.root.destroy()
            self.root = None