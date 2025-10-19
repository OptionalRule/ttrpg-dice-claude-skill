"""Tests for dice evaluation and RNG"""
import pytest


class TestDiceRolling:
    """Test basic dice rolling functionality"""

    def test_roll_returns_valid_range(self, roll):
        """Test that rolls are within valid range"""
        for _ in range(50):
            result = roll("1d6")
            assert 1 <= result["final"] <= 6

    def test_multiple_dice(self, roll):
        """Test rolling multiple dice"""
        result = roll("5d6")
        assert 5 <= result["final"] <= 30
        assert len(result["trace"][0]["rolls"]) == 5

    def test_different_die_sizes(self, roll):
        """Test different die sizes"""
        test_cases = [
            ("1d4", 1, 4),
            ("1d6", 1, 6),
            ("1d8", 1, 8),
            ("1d10", 1, 10),
            ("1d12", 1, 12),
            ("1d20", 1, 20),
            ("1d100", 1, 100),
        ]
        for expr, min_val, max_val in test_cases:
            result = roll(expr)
            assert min_val <= result["final"] <= max_val


class TestTraceInformation:
    """Test that trace information is complete and accurate"""

    def test_trace_includes_all_rolls(self, roll):
        """Test that trace includes all individual die rolls"""
        result = roll("4d6")
        assert len(result["trace"]) > 0
        assert len(result["trace"][0]["rolls"]) == 4

    def test_trace_includes_sum(self, roll):
        """Test that trace includes the sum"""
        result = roll("3d6")
        rolls = result["trace"][0]["rolls"]
        expected_sum = sum(r["value"] for r in rolls)
        assert result["trace"][0]["sum"] == expected_sum

    def test_trace_includes_term(self, roll):
        """Test that trace includes the original term"""
        result = roll("2d8+3")
        assert any("2d8" in trace["term"] for trace in result["trace"])

    def test_rng_metadata(self, roll):
        """Test that RNG metadata is included"""
        result = roll("1d6")
        assert "rng" in result
        assert result["rng"]["source"] == "CSPRNG"
        assert result["rng"]["method"] == "rejectionSampling"

    def test_limits_metadata(self, roll):
        """Test that limits metadata is included"""
        result = roll("1d6")
        assert "limits" in result
        assert result["limits"]["maxDice"] == 1000
        assert result["limits"]["maxExplosions"] == 100

    def test_version_included(self, roll):
        """Test that version is included in response"""
        result = roll("1d6")
        assert "version" in result
        assert result["version"].startswith("dice-")


class TestMultipleTerms:
    """Test expressions with multiple dice terms"""

    def test_two_different_dice(self, roll):
        """Test rolling two different types of dice"""
        result = roll("1d6+1d8")
        assert 2 <= result["final"] <= 14
        assert len(result["trace"]) == 2

    def test_three_dice_terms(self, roll):
        """Test three different dice terms"""
        result = roll("1d4+1d6+1d8")
        assert 3 <= result["final"] <= 18
        assert len(result["trace"]) == 3

    def test_dice_with_constants(self, roll):
        """Test dice mixed with constants"""
        result = roll("2d6+5")
        assert 7 <= result["final"] <= 17
