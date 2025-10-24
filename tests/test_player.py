"""
Unit tests for the Player class from src.core.player.py using pytest.
"""

import pytest
import uuid
from src.core.player import Player


@pytest.fixture
def default_player():
    """Fixture for a default Player instance."""
    return Player()

@pytest.fixture
def custom_player():
    """Fixture for a Player instance with a custom name."""
    return Player("Gamer X")

def test_player_initialization_default(default_player):
    """Test player initialization with default values."""
    assert default_player.name == "Player"
    assert default_player.current_score == 0
    assert isinstance(default_player.player_id, str)
    # Check if player_id is a valid UUID
    assert len(default_player.player_id) == 36 and default_player.player_id.count('-') == 4

def test_player_initialization_custom_name(custom_player):
    """Test player initialization with a custom name."""
    assert custom_player.name == "Gamer X"
    assert custom_player.current_score == 0

def test_player_initialization_whitespace_trimming():
    """Test that leading/trailing whitespace is trimmed from the name."""
    player = Player("  Whitespace Warrior  ")
    assert player.name == "Whitespace Warrior"

def test_player_initialization_empty_name_defaults():
    """Test that an empty name string defaults to 'Player'."""
    player_empty = Player("")
    player_space = Player("   ")
    assert player_empty.name == "Player"
    assert player_space.name == "Player"

def test_player_id_is_unique():
    """Test that each player instance gets a unique ID."""
    player1 = Player("P1")
    player2 = Player("P2")
    assert player1.player_id != player2.player_id

def test_name_setter_success(default_player):
    """Test setting a new valid name."""
    default_player.name = "New Name"
    assert default_player.name == "New Name"

def test_name_setter_whitespace_trimming(default_player):
    """Test that the setter trims whitespace."""
    default_player.name = " Trimmed "
    assert default_player.name == "Trimmed"

def test_name_setter_raises_error_on_empty(default_player):
    """Test that setting an empty name raises ValueError."""
    with pytest.raises(ValueError, match="Player name cannot be empty"):
        default_player.name = ""

def test_name_setter_raises_error_on_whitespace_only(default_player):
    """Test that setting a whitespace-only name raises ValueError."""
    with pytest.raises(ValueError, match="Player name cannot be empty"):
        default_player.name = "  "

def test_set_name_safely_success(default_player):
    """Test safe name setting with a valid name."""
    result = default_player.set_name_safely("Safe Name")
    assert result is True
    assert default_player.name == "Safe Name"

def test_set_name_safely_failure(default_player):
    """Test safe name setting with an invalid name (should return False)."""
    original_name = default_player.name
    result = default_player.set_name_safely(" ")
    assert result is False
    # Ensure the name was not changed
    assert default_player.name == original_name

def test_create_player_with_name_success():
    """Test successful player creation using the class method."""
    player = Player.create_player_with_name("Test Creator")
    assert isinstance(player, Player)
    assert player.name == "Test Creator"

def test_create_player_with_name_failure():
    """Test fallback to default name"""
    player = Player.create_player_with_name(" ")
    assert player.name == "Player"

def test_add_to_score_positive(default_player):
    """Test adding positive points to the score."""
    default_player.add_to_score(10)
    assert default_player.current_score == 10
    default_player.add_to_score(5)
    assert default_player.current_score == 15

def test_add_to_score_zero(default_player):
    """Test adding zero points to the score."""
    default_player.set_score(50)
    default_player.add_to_score(0)
    assert default_player.current_score == 50

def test_add_to_score_negative_raises_error(default_player):
    """Test that adding negative points raises ValueError."""
    with pytest.raises(ValueError, match="Points cannot be negative"):
        default_player.add_to_score(-5)

def test_reset_score(default_player):
    """Test resetting the score to zero."""
    default_player.set_score(99)
    default_player.reset_score()
    assert default_player.current_score == 0

def test_set_score_valid(default_player):
    """Test setting a valid positive score directly."""
    default_player.set_score(75)
    assert default_player.current_score == 75

def test_set_score_zero(default_player):
    """Test setting a score to zero."""
    default_player.set_score(0)
    assert default_player.current_score == 0

def test_set_score_negative_raises_error(default_player):
    """Test that setting a negative score raises ValueError."""
    with pytest.raises(ValueError, match="Score cannot be negative"):
        default_player.set_score(-10)

def test_str_representation(custom_player):
    """Test the __str__ method output."""
    custom_player.set_score(25)
    expected_str = "Player(name='Gamer X', score=25)"
    assert str(custom_player) == expected_str

def test_repr_representation(custom_player):
    """Test the __repr__ method output."""
    custom_player.set_score(25)
    expected_repr = "Player(name='Gamer X', current_score=25)"
    assert repr(custom_player) == expected_repr

def test_current_score_getter(custom_player):
    """Test the current_score getter property."""
    custom_player.add_to_score(100)
    assert custom_player.current_score == 100