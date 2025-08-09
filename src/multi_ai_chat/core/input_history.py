"""
Multi-AI Chat Manager v1.0.0 - Input History Manager
 history management with file persistence
"""

import os
import logging
from typing import List, Optional
from datetime import datetime

class InputHistoryManager:
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Settings
        history_config = config.get('history', {})
        self.max_entries = history_config.get('max_entries', 100)
        self.save_to_file = history_config.get('save_to_file', True)
        self.history_file = history_config.get('history_file', 'data/input_history.txt')
        
        # Ensure data directory exists
        self._ensure_data_directory()
        
        # History storage
        self.history: List[dict] = []
        self.current_index = -1
        
        # Load existing history
        self._load_history()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists"""
        try:
            data_dir = os.path.dirname(self.history_file)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir)
                self.logger.info(f"Created data directory: {data_dir}")
        except Exception as e:
            self.logger.error(f"Error creating data directory: {e}")
    
    def add_entry(self, prompt: str) -> None:
        """Add a new prompt to history"""
        if not prompt or not prompt.strip():
            return
        
        prompt = prompt.strip()
        
        # Avoid duplicate consecutive entries
        if self.history and self.history[-1]['prompt'] == prompt:
            return
        
        # Create entry
        entry = {
            'prompt': prompt,
            'timestamp': datetime.now().isoformat(),
            'length': len(prompt)
        }
        
        # Add to history
        self.history.append(entry)
        
        # Maintain max entries
        if len(self.history) > self.max_entries:
            self.history.pop(0)
        
        # Reset index
        self.current_index = len(self.history)
        
        # Save to file
        if self.save_to_file:
            self._save_history()
        
        self.logger.debug(f"Added to history: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
    
    def get_previous(self) -> Optional[str]:
        """Get previous entry"""
        if not self.history:
            return None
        
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = 0
        
        return self.history[self.current_index]['prompt']
    
    def get_next(self) -> Optional[str]:
        """Get next entry"""
        if not self.history:
            return None
        
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]['prompt']
        else:
            self.current_index = len(self.history)
            return ""
    
    def get_all_entries(self) -> List[dict]:
        """Get all history entries"""
        return self.history.copy()
    
    def get_recent_entries(self, count: int = 10) -> List[dict]:
        """Get recent history entries"""
        return self.history[-count:] if self.history else []
    
    def search_history(self, search_term: str) -> List[dict]:
        """Search history for entries containing the search term"""
        if not search_term.strip():
            return []
        
        search_term = search_term.lower()
        matching_entries = []
        
        for entry in self.history:
            if search_term in entry['prompt'].lower():
                matching_entries.append(entry)
        
        return matching_entries
    
    def clear_history(self) -> None:
        """Clear all history entries"""
        self.history.clear()
        self.current_index = -1
        
        if self.save_to_file:
            self._save_history()
        
        self.logger.info("History cleared")
    
    def get_stats(self) -> dict:
        """Get history statistics"""
        if not self.history:
            return {
                'total_entries': 0,
                'avg_length': 0,
                'oldest_entry': None,
                'newest_entry': None,
                'total_characters': 0
            }
        
        total_length = sum(entry['length'] for entry in self.history)
        avg_length = total_length / len(self.history)
        
        return {
            'total_entries': len(self.history),
            'avg_length': round(avg_length, 1),
            'oldest_entry': self.history[0]['timestamp'] if self.history else None,
            'newest_entry': self.history[-1]['timestamp'] if self.history else None,
            'total_characters': total_length
        }
    
    def export_history(self, export_path: str) -> bool:
        """Export history to a specified file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write("# Multi-AI Chat Manager - Exported Prompt History\n")
                f.write(f"# Exported on: {datetime.now().isoformat()}\n")
                f.write(f"# Total entries: {len(self.history)}\n\n")
                
                for i, entry in enumerate(self.history, 1):
                    f.write(f"Entry {i}:\n")
                    f.write(f"Timestamp: {entry['timestamp']}\n")
                    f.write(f"Length: {entry['length']} characters\n")
                    f.write(f"Prompt: {entry['prompt']}\n")
                    f.write("-" * 50 + "\n\n")
            
            self.logger.info(f"History exported to: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting history: {e}")
            return False
    
    def _load_history(self) -> None:
        """Load history from file"""
        if not self.save_to_file or not os.path.exists(self.history_file):
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    # Parse timestamped entry
                    if ' | ' in line:
                        timestamp_str, prompt = line.split(' | ', 1)
                        entry = {
                            'prompt': prompt,
                            'timestamp': timestamp_str,
                            'length': len(prompt)
                        }
                    else:
                        # Fallback for simple format
                        entry = {
                            'prompt': line,
                            'timestamp': datetime.now().isoformat(),
                            'length': len(line)
                        }
                    
                    self.history.append(entry)
                    
                except Exception as e:
                    self.logger.debug(f"Error parsing history line: {e}")
                    continue
            
            # Maintain max entries
            if len(self.history) > self.max_entries:
                self.history = self.history[-self.max_entries:]
            
            self.current_index = len(self.history)
            self.logger.info(f"Loaded {len(self.history)} history entries from {self.history_file}")
            
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
    
    def _save_history(self) -> None:
        """Save history to file"""
        if not self.save_to_file:
            return
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                # Write header comment
                f.write(f"# Multi-AI Chat Manager v1.0.0 - Prompt History\n")
                f.write(f"# Last updated: {datetime.now().isoformat()}\n")
                f.write(f"# Total entries: {len(self.history)}\n\n")
                
                # Write history entries
                for entry in self.history:
                    line = f"{entry['timestamp']} | {entry['prompt']}\n"
                    f.write(line)
            
            self.logger.debug(f"History saved to {self.history_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")
    
    def get_file_path(self) -> str:
        """Get the full path to the history file"""
        return os.path.abspath(self.history_file)
    
    def is_file_accessible(self) -> bool:
        """Check if the history file is accessible"""
        try:
            # Try to create/access the file
            with open(self.history_file, 'a', encoding='utf-8'):
                pass
            return True
        except Exception as e:
            self.logger.error(f"History file not accessible: {e}")
            return False