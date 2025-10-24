# import os
# import json
# import pytest
# from datetime import datetime
# from unittest.mock import MagicMock, patch
# from typing import Dict, Any, List, Tuple, Optional
#
#
# # The SaveManager class provided by the user, included here for testing completeness.
# class SaveManager:
#     """Manages game save and load functionality."""
#
#     def __init__(self, saves_dir: str = "saves"):
#         """
#         Initialize the save manager.
#
#         Args:
#             saves_dir (str): Directory to store save files.
#         """
#         self._saves_dir = saves_dir
#         if not os.path.exists(self._saves_dir):
#             os.makedirs(self._saves_dir)
#
#     def save_game(self, game_state: Dict[str, Any], filename: str = None) -> str:
#         """
#         Save the current game state to a JSON file.
#
#         Args:
#             game_state (Dict): The game state to save.
#             filename (str, optional): Custom filename. If None, uses auto-generated name.
#
#         Returns:
#             str: Status message about the save operation.
#         """
#         try:
#             if filename is None:
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 filename = f"pig_game_save_{timestamp}.json"
#
#             filepath = os.path.join(self._saves_dir, filename)
#
#             with open(filepath, "w") as f:
#                 json.dump(game_state, f, indent=2)
#
#             return f"Game saved successfully to '{filename}'!"
#
#         except Exception as e:
#             return f"Failed to save game: {str(e)}"
#
#     def load_game(self, filename: str) -> Tuple[Optional[Dict[str, Any]], str]:
#         """
#         Load a saved game state from a JSON file.
#
#         Args:
#             filename (str): The filename of the save file to load.
#
#         Returns:
#             Tuple[Optional[Dict], str]: Game state dict (or None) and status message.
#         """
#         try:
#             filepath = os.path.join(self._saves_dir, filename)
#
#             if not os.path.exists(filepath):
#                 return None, f"Save file '{filename}' not found."
#
#             with open(filepath, "r") as f:
#                 save_data = json.load(f)
#
#             return save_data, f"Game loaded successfully from '{filename}'!"
#
#         except Exception as e:
#             return None, f"Failed to load game: {str(e)}"
#
#     def list_save_files(self) -> List[str]:
#         """
#         Get a list of available save files.
#
#         Returns:
#             List[str]: List of save filenames.
#         """
#         if not os.path.exists(self._saves_dir):
#             return []
#
#         save_files = []
#         for filename in os.listdir(self._saves_dir):
#             if filename.endswith(".json"):
#                 save_files.append(filename)
#
#         return sorted(save_files, reverse=True)
#
#
# # --- Pytest Fixtures and Test Class ---
#
# # Mock datetime for deterministic filenames
# @pytest.fixture
# def mock_datetime():
#     with patch("src.managers.save_manager.datetime") as mock_dt:
#         mock_dt.now.return_value.strftime.return_value = "20251024_100000"
#         yield mock_dt
#
#
# # Mock the entire os module behavior for isolation
# @pytest.fixture
# def mock_os():
#     with patch("src.managers.save_manager.os") as mock_os:
#         mock_os.path.exists.return_value = True
#         mock_os.path.join.side_effect = lambda *args: "/".join(args)
#         yield mock_os
#
#
# # Mock the json module behavior
# @pytest.fixture
# def mock_json():
#     with patch("src.managers.save_manager.json") as mock_json:
#         yield mock_json
#
#
# # Mock the open function and file handle
# @pytest.fixture
# def mock_open():
#     with patch("src.managers.save_manager.open", new_callable=MagicMock) as mock_file:
#         yield mock_file
#
#
# @pytest.fixture
# def manager(mock_os):
#     """Fixture to create a SaveManager instance."""
#     # Ensure SaveManager is initialized with the mocked os, but we'll use a unique path
#     return SaveManager("mock_saves")
#
#
# class TestSaveManager:
#     """Tests for the SaveManager class."""
#
#     SAVE_DIR = "mock_saves"
#     GAME_STATE = {"player": "Alice", "score": 50}
#
#     # --- Initialization Tests ---
#     def test_init_directory_exists(self, mock_os):
#         """Test initialization when the saves directory already exists."""
#         mock_os.path.exists.return_value = True
#         SaveManager(self.SAVE_DIR)
#         mock_os.makedirs.assert_not_called()
#
#     def test_init_directory_does_not_exist(self, mock_os):
#         """Test initialization when the saves directory does not exist."""
#         mock_os.path.exists.return_value = False
#         SaveManager(self.SAVE_DIR)
#         mock_os.makedirs.assert_called_once_with(self.SAVE_DIR)
#
#     # --- Save Game Tests ---
#     def test_save_game_auto_filename(self, manager, mock_os, mock_json, mock_open, mock_datetime):
#         """Test saving a game using an auto-generated timestamped filename."""
#         result = manager.save_game(self.GAME_STATE)
#         expected_filename = "pig_game_save_20251024_100000.json"
#         expected_filepath = f"{self.SAVE_DIR}/{expected_filename}"
#
#         mock_open.assert_called_once_with(expected_filepath, "w")
#         mock_json.dump.assert_called_once_with(self.GAME_STATE, mock_open(), indent=2)
#         assert result == f"Game saved successfully to '{expected_filename}'!"
#
#     def test_save_game_custom_filename(self, manager, mock_os, mock_json, mock_open):
#         """Test saving a game using a custom filename."""
#         custom_name = "test_run_1.json"
#         result = manager.save_game(self.GAME_STATE, custom_name)
#         expected_filepath = f"{self.SAVE_DIR}/{custom_name}"
#
#         mock_open.assert_called_once_with(expected_filepath, "w")
#         mock_json.dump.assert_called_once_with(self.GAME_STATE, mock_open(), indent=2)
#         assert result == f"Game saved successfully to '{custom_name}'!"
#
#     def test_save_game_failure(self, manager, mock_os, mock_open):
#         """Test failure handling during the save operation."""
#         mock_open.side_effect = IOError("Permission denied")
#         result = manager.save_game(self.GAME_STATE, "error.json")
#         assert "Failed to save game: Permission denied" in result
#
#     # --- Load Game Tests ---
#     def test_load_game_success(self, manager, mock_os, mock_json, mock_open):
#         """Test loading a saved game successfully."""
#         mock_os.path.exists.return_value = True
#         mock_json.load.return_value = self.GAME_STATE
#         filename = "valid_save.json"
#
#         data, message = manager.load_game(filename)
#         expected_filepath = f"{self.SAVE_DIR}/{filename}"
#
#         mock_os.path.exists.assert_called_once_with(expected_filepath)
#         mock_open.assert_called_once_with(expected_filepath, "r")
#         mock_json.load.assert_called_once()
#
#         assert data == self.GAME_STATE
#         assert message == f"Game loaded successfully from '{filename}'!"
#
#     def test_load_game_file_not_found(self, manager, mock_os, mock_json):
#         """Test loading a file that does not exist."""
#         mock_os.path.exists.return_value = False
#         filename = "missing.json"
#
#         data, message = manager.load_game(filename)
#
#         assert data is None
#         assert message == f"Save file '{filename}' not found."
#         mock_json.load.assert_not_called()
#
#     def test_load_game_failure(self, manager, mock_os, mock_json, mock_open):
#         """Test failure handling during the load operation (e.g., corrupted JSON)."""
#         mock_os.path.exists.return_value = True
#         mock_json.load.side_effect = json.JSONDecodeError("Bad format", doc="data", pos=0)
#         filename = "corrupt.json"
#
#         data, message = manager.load_game(filename)
#
#         assert data is None
#         assert "Failed to load game: Bad format" in message
#
#     # --- List Files Tests ---
#     def test_list_save_files_with_files(self, manager, mock_os):
#         """Test listing files when multiple save files are present."""
#         mock_os.listdir.return_value = [
#             "pig_game_save_20251025.json",
#             "pig_game_save_20251024.json",
#             "log.txt",
#             "temp.json",
#         ]
#
#         # Should be sorted in reverse (newest first) and only include .json files
#         expected = [
#             "temp.json",
#             "pig_game_save_20251025.json",
#             "pig_game_save_20251024.json",
#         ]
#
#         files = manager.list_save_files()
#         assert files == expected
#
#     def test_list_save_files_no_files(self, manager, mock_os):
#         """Test listing files when the directory is empty."""
#         mock_os.listdir.return_value = ["log.txt", "temp.log"]
#         files = manager.list_save_files()
#         assert files == []
#
#     def test_list_save_files_dir_not_exist(self, manager, mock_os):
#         """Test listing files when the saves directory does not exist."""
#         mock_os.path.exists.return_value = False
#         files = manager.list_save_files()
#         assert files == []
#         mock_os.listdir.assert_not_called()
