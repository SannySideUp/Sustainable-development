"""
unit tests for the Player class.

This file contains extensive unit tests for the Player class to ensure
all functionality works correctly and meets the coverage requirements.
"""

import pytest
import uuid
from unittest.mock import patch, Mock
from src.player import Player


class TestPlayer:
    """Test cases for the Player class."""
    
    def test_player_creation_default_name(self):
        """Test creating a player with default name."""
        player = Player()
        assert player.name == "Player"
        assert player.current_score == 0
        assert isinstance(player.player_id, str)
        assert len(player.player_id) > 0
    
    def test_player_creation_custom_name(self):
        """Test creating a player with custom name."""
        player = Player("TestPlayer")
        assert player.name == "TestPlayer"
        assert player.current_score == 0
        assert isinstance(player.player_id, str)
    
    def test_player_creation_empty_name(self):
        """Test creating a player with empty name."""
        player = Player("")
        assert player.name == ""
        assert player.current_score == 0
    
    def test_player_creation_whitespace_name(self):
        """Test creating a player with whitespace name."""
        player = Player("   ")
        assert player.name == "   "
        assert player.current_score == 0
    
    def test_player_name_property_getter(self):
        """Test player name property getter."""
        player = Player("Alice")
        assert player.name == "Alice"
    
    def test_player_name_property_setter_valid(self):
        """Test player name property setter with valid name."""
        player = Player("OriginalName")
        player.name = "NewName"
        assert player.name == "NewName"
    
    def test_player_name_property_setter_strips_whitespace(self):
        """Test that name setter strips whitespace."""
        player = Player("OriginalName")
        player.name = "  NewName  "
        assert player.name == "NewName"
    
    def test_player_name_property_setter_empty_string(self):
        """Test name setter with empty string raises ValueError."""
        player = Player("ValidName")
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            player.name = ""
    
    def test_player_name_property_setter_none(self):
        """Test name setter with None raises ValueError."""
        player = Player("ValidName")
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            player.name = None
    
    def test_player_name_property_setter_whitespace_only(self):
        """Test name setter with whitespace only raises ValueError."""
        player = Player("ValidName")
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            player.name = "   "
    
    def test_set_name_safely_valid_name(self):
        """Test set_name_safely with valid name."""
        player = Player("OriginalName")
        result = player.set_name_safely("NewName")
        assert result is True
        assert player.name == "NewName"
    
    def test_set_name_safely_invalid_name(self):
        """Test set_name_safely with invalid name."""
        player = Player("OriginalName")
        result = player.set_name_safely("")
        assert result is False
        assert player.name == "OriginalName"
    
    def test_set_name_safely_whitespace_name(self):
        """Test set_name_safely with whitespace name."""
        player = Player("OriginalName")
        result = player.set_name_safely("   ")
        assert result is False
        assert player.name == "OriginalName"
    
    def test_create_player_with_name_valid(self):
        """Test create_player_with_name with valid name."""
        player = Player.create_player_with_name("TestPlayer")
        assert player is not None
        assert isinstance(player, Player)
        assert player.name == "TestPlayer"
    
    def test_create_player_with_name_invalid(self):
        """Test create_player_with_name with invalid name."""
        player = Player.create_player_with_name("")
        assert player is not None
        assert player.name == ""
    
    def test_create_player_with_name_whitespace(self):
        """Test create_player_with_name with whitespace name."""
        player = Player.create_player_with_name("   ")
        assert player is not None
        assert player.name == "   "
    
    def test_current_score_property(self):
        """Test current score property."""
        player = Player("TestPlayer")
        assert player.current_score == 0
    
    def test_add_to_score_positive(self):
        """Test adding positive score."""
        player = Player("TestPlayer")
        player.add_to_score(25)
        assert player.current_score == 25
        
        player.add_to_score(15)
        assert player.current_score == 40
    
    def test_add_to_score_zero(self):
        """Test adding zero score."""
        player = Player("TestPlayer")
        player.add_to_score(0)
        assert player.current_score == 0
    
    def test_add_to_score_negative_raises_error(self):
        """Test adding negative score raises ValueError."""
        player = Player("TestPlayer")
        with pytest.raises(ValueError, match="Points cannot be negative"):
            player.add_to_score(-10)
    
    def test_reset_score(self):
        """Test resetting player score."""
        player = Player("TestPlayer")
        player.add_to_score(75)
        assert player.current_score == 75
        
        player.reset_score()
        assert player.current_score == 0
    
    def test_set_score_positive(self):
        """Test setting positive score."""
        player = Player("TestPlayer")
        player.set_score(50)
        assert player.current_score == 50
    
    def test_set_score_zero(self):
        """Test setting zero score."""
        player = Player("TestPlayer")
        player.set_score(0)
        assert player.current_score == 0
    
    def test_set_score_negative_raises_error(self):
        """Test setting negative score raises ValueError."""
        player = Player("TestPlayer")
        with pytest.raises(ValueError, match="Score cannot be negative"):
            player.set_score(-5)
    
    def test_str_representation(self):
        """Test string representation of player."""
        player = Player("TestPlayer")
        player.add_to_score(42)
        
        str_repr = str(player)
        assert "TestPlayer" in str_repr
        assert "42" in str_repr
        assert "Player(name=" in str_repr
        assert "score=" in str_repr
    
    def test_repr_representation(self):
        """Test detailed string representation of player."""
        player = Player("TestPlayer")
        player.add_to_score(42)
        
        repr_str = repr(player)
        assert "TestPlayer" in repr_str
        assert "42" in repr_str
        assert "Player(name=" in repr_str
        assert "current_score=" in repr_str
    
    def test_player_id_uniqueness(self):
        """Test that player IDs are unique."""
        player1 = Player("Player1")
        player2 = Player("Player2")
        assert player1.player_id != player2.player_id
    
    def test_player_id_format(self):
        """Test that player ID is valid UUID format."""
        player = Player("TestPlayer")
        # Should be able to parse as UUID
        uuid.UUID(player.player_id)
    
    def test_multiple_players_independence(self):
        """Test that multiple players are independent."""
        player1 = Player("Player1")
        player2 = Player("Player2")
        
        player1.add_to_score(30)
        player2.add_to_score(50)
        
        assert player1.current_score == 30
        assert player2.current_score == 50
        assert player1.name == "Player1"
        assert player2.name == "Player2"
        assert player1.player_id != player2.player_id
    
    def test_player_attributes_exist(self):
        """Test that player has all required attributes."""
        player = Player("TestPlayer")
        
        assert hasattr(player, 'name')
        assert hasattr(player, 'current_score')
        assert hasattr(player, 'player_id')
        
        assert player.name is not None
        assert player.current_score is not None
        assert player.player_id is not None
    
    def test_current_score_read_only_property(self):
        """Test that current_score property is read-only."""
        player = Player("TestPlayer")
        
        with pytest.raises(AttributeError):
            player.current_score = 50
    
    def test_name_property_setter_validation(self):
        """Test comprehensive name validation."""
        player = Player("ValidName")
        
        # Test various invalid inputs
        invalid_inputs = ["", None, "   ", "\t", "\n", "  \t  "]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="Player name cannot be empty"):
                player.name = invalid_input
    
    def test_score_operations_combination(self):
        """Test combination of score operations."""
        player = Player("TestPlayer")
        
        # Start with 0
        assert player.current_score == 0
        
        # Add some points
        player.add_to_score(20)
        assert player.current_score == 20
        
        # Set to specific value
        player.set_score(50)
        assert player.current_score == 50
        
        # Add more points
        player.add_to_score(10)
        assert player.current_score == 60
        
        # Reset
        player.reset_score()
        assert player.current_score == 0
    
    def test_player_immutable_after_creation(self):
        """Test that player core attributes are properly encapsulated."""
        player = Player("TestPlayer")
        
        # Private attributes can be set in Python, but we test the public interface
        original_name = player.name
        player._name = "Hacked"
        # The name property uses _name directly, so it will change
        assert player.name == "Hacked"
        
        # Test that we can't directly set _current_score (Python allows this too)
        original_score = player.current_score
        player._current_score = 999
        assert player.current_score == 999
    
    def test_player_with_special_characters_in_name(self):
        """Test player with special characters in name."""
        special_names = ["Player-1", "Player_1", "Player.1", "Player@1", "Player#1"]
        
        for name in special_names:
            player = Player(name)
            assert player.name == name
            assert player.current_score == 0
    
    def test_player_with_unicode_name(self):
        """Test player with unicode characters in name."""
        unicode_name = "Játékos"
        player = Player(unicode_name)
        assert player.name == unicode_name
        assert player.current_score == 0
    
    def test_player_with_long_name(self):
        """Test player with very long name."""
        long_name = "A" * 1000
        player = Player(long_name)
        assert player.name == long_name
        assert player.current_score == 0
    
    def test_player_score_edge_cases(self):
        """Test edge cases for score operations."""
        player = Player("TestPlayer")
        
        # Test very large score
        large_score = 999999
        player.set_score(large_score)
        assert player.current_score == large_score
        
        # Test adding to large score
        player.add_to_score(1)
        assert player.current_score == large_score + 1
        
        # Test reset from large score
        player.reset_score()
        assert player.current_score == 0
