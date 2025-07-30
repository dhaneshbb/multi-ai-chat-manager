"""
Input History Manager for Multi-AI Chat Manager
Simple history management with file persistence
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
        self.history_file = history_config.get('history_file', 'input_history.txt')
        
        # History storage
        self.history: List[dict] = []
        self.current_index = -1
        
        # Load existing history
        self._load_history()
    
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
    
    def get_stats(self) -> dict:
        """Get history statistics"""
        if not self.history:
            return {
                'total_entries': 0,
                'avg_length': 0,
                'oldest_entry': None,
                'newest_entry': None
            }
        
        total_length = sum(entry['length'] for entry in self.history)
        avg_length = total_length / len(self.history)
        
        return {
            'total_entries': len(self.history),
            'avg_length': round(avg_length, 1),
            'oldest_entry': self.history[0]['timestamp'] if self.history else None,
            'newest_entry': self.history[-1]['timestamp'] if self.history else None
        }
    
    def _load_history(self) -> None:
        """Load history from file"""
        if not self.save_to_file or not os.path.exists(self.history_file):
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
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
            self.logger.info(f"Loaded {len(self.history)} history entries")
            
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
    
    def _save_history(self) -> None:
        """Save history to file"""
        if not self.save_to_file:
            return
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for entry in self.history:
                    line = f"{entry['timestamp']} | {entry['prompt']}\n"
                    f.write(line)
            
            self.logger.debug(f"History saved to {self.history_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")