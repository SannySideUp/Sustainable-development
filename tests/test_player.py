"""
Test file for the Player class.

This module contains comprehensive unit tests for the Player class
to ensure all functionality works correctly.
"""

import pytest
from src.player import Player


class TestPlayer:
    """Test cases for the Player class."""
    
    def test_player_creation_default_name(self):
        """Test creating a player with default name."""
        player = Player()
        assert player.name == "Player"
        assert player.current_score == 0
        assert hasattr(player, 'player_id')
    
    def test_player_creation_custom_name(self):
        """Test creating a player with custom name."""
        player = Player("TestPlayer")
        assert player.name == "TestPlayer"
        assert player.current_score == 0
    
    def test_player_name_property(self):
        """Test player name property."""
        player = Player("Alice")
        assert player.name == "Alice"
        
        player.name = "Bob"
        assert player.name == "Bob"
    
    def test_player_name_validation(self):
        """Test player name validation."""
        player = Player("ValidName")
        assert player.name == "ValidName"
        
        with pytest.raises(ValueError):
            player.name = ""
        
        with pytest.raises(ValueError):
            player.name = None
    
    def test_current_score_property(self):
        """Test current score property."""
        player = Player("TestPlayer")
        assert player.current_score == 0
        
        player.set_score(50)
        assert player.current_score == 50
    
    def test_current_score_validation(self):
        """Test current score validation."""
        player = Player("TestPlayer")
        
        with pytest.raises(ValueError):
            player.set_score(-10)
    
    def test_add_score(self):
        """Test adding score to player."""
        player = Player("TestPlayer")
        assert player.current_score == 0
        
        player.add_to_score(25)
        assert player.current_score == 25
        
        player.add_to_score(15)
        assert player.current_score == 40
    
    def test_add_score_negative(self):
        """Test adding negative score."""
        player = Player("TestPlayer")
        player.set_score(50)
        
        with pytest.raises(ValueError):
            player.add_to_score(-10)
    
    def test_reset_score(self):
        """Test resetting player score."""
        player = Player("TestPlayer")
        player.set_score(75)
        
        player.reset_score()
        assert player.current_score == 0
    
    def test_set_score(self):
        """Test setting score directly."""
        player = Player("TestPlayer")
        player.set_score(100)
        assert player.current_score == 100
    
    def test_set_score_negative(self):
        """Test setting negative score."""
        player = Player("TestPlayer")
        
        with pytest.raises(ValueError):
            player.set_score(-50)
    
    def test_set_name_safely(self):
        """Test setting name safely."""
        player = Player("OriginalName")
        
        result = player.set_name_safely("NewName")
        assert result is True
        assert player.name == "NewName"
        
        result = player.set_name_safely("")
        assert result is False
        assert player.name == "NewName"
    
    def test_create_player_with_name(self):
        """Test creating player with name safely."""
        player = Player.create_player_with_name("ValidName")
        assert player is not None
        assert player.name == "ValidName"
        
        player = Player.create_player_with_name("")
        assert player is not None
    
    def test_str_representation(self):
        """Test string representation of player."""
        player = Player("TestPlayer")
        player.set_score(42)
        
        str_repr = str(player)
        assert "TestPlayer" in str_repr
        assert "42" in str_repr
    
    def test_player_id_uniqueness(self):
        """Test that player IDs are unique."""
        player1 = Player("Player1")
        player2 = Player("Player2")
        
        assert player1.player_id != player2.player_id
        assert isinstance(player1.player_id, str)
        assert isinstance(player2.player_id, str)
    
    def test_player_equality(self):
        """Test player equality."""
        player1 = Player("SameName")
        player2 = Player("SameName")
        
        assert player1 != player2
    
    def test_player_attributes(self):
        """Test that player has all required attributes."""
        player = Player("TestPlayer")
        
        assert hasattr(player, 'name')
        assert hasattr(player, 'current_score')
        assert hasattr(player, 'player_id')
        
        assert player.name is not None
        assert player.current_score is not None
        assert player.player_id is not None
