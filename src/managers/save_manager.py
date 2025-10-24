import os
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
import json

class SaveManager:
    """Manages game save and load functionality."""
    
    def __init__(self, saves_dir: str = "saves"):
        """
        Initialize the save manager.
        
        Args:
            saves_dir (str): Directory to store save files.
        """
        self._saves_dir = saves_dir
        if not os.path.exists(self._saves_dir):
            os.makedirs(self._saves_dir)
    
    def save_game(self, game_state: Dict[str, Any], filename: str = None) -> str:
        """
        Save the current game state to a JSON file.
        
        Args:
            game_state (Dict): The game state to save.
            filename (str, optional): Custom filename. If None, uses auto-generated name.
            
        Returns:
            str: Status message about the save operation.
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pig_game_save_{timestamp}.json"
            
            filepath = os.path.join(self._saves_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(game_state, f, indent=2)
            
            return f"Game saved successfully to '{filename}'!"
            
        except Exception as e:
            return f"Failed to save game: {str(e)}"
    
    def load_game(self, filename: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Load a saved game state from a JSON file.
        
        Args:
            filename (str): The filename of the save file to load.
            
        Returns:
            Tuple[Optional[Dict], str]: Game state dict (or None) and status message.
        """
        try:
            filepath = os.path.join(self._saves_dir, filename)
            
            if not os.path.exists(filepath):
                return None, f"Save file '{filename}' not found."
            
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            return save_data, f"Game loaded successfully from '{filename}'!"
            
        except Exception as e:
            return None, f"Failed to load game: {str(e)}"
    
    def list_save_files(self) -> List[str]:
        """
        Get a list of available save files.
        
        Returns:
            List[str]: List of save filenames.
        """
        if not os.path.exists(self._saves_dir):
            return []
        
        save_files = []
        for filename in os.listdir(self._saves_dir):
            if filename.endswith('.json'):
                save_files.append(filename)
        
        return sorted(save_files, reverse=True)
