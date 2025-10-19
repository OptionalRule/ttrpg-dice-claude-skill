"""Tests for FATE/Fudge dice"""
import pytest


class TestFateDice:
    """Test FATE/Fudge dice (dF) functionality"""

    def test_basic_fate_roll(self, roll):
        """Test basic FATE dice roll (4dF)"""
        result = roll("4dF")
        assert result["ok"] is True
        assert -4 <= result["final"] <= 4
        assert len(result["trace"][0]["rolls"]) == 4

    def test_fate_dice_values(self, roll):
        """Test that FATE dice return valid values (-1, 0, +1)"""
        result = roll("10dF")
        for r in result["trace"][0]["rolls"]:
            assert r["value"] in [-1, 0, 1]

    def test_single_fate_die(self, roll):
        """Test single FATE die"""
        result = roll("1dF")
        assert result["final"] in [-1, 0, 1]

    def test_fate_with_positive_modifier(self, roll):
        """Test FATE with positive skill modifier"""
        result = roll("4dF+3")
        assert result["ok"] is True
        assert -1 <= result["final"] <= 7  # -4+3 to 4+3

    def test_fate_with_negative_modifier(self, roll):
        """Test FATE with negative skill modifier"""
        result = roll("4dF-2")
        assert result["ok"] is True
        assert -6 <= result["final"] <= 2  # -4-2 to 4-2

    def test_fate_multiple_rolls(self, roll):
        """Test that multiple FATE rolls produce different results"""
        results = [roll("4dF")["final"] for _ in range(20)]
        # With 20 rolls, we should see some variation
        assert len(set(results)) > 1

    def test_fate_average_distribution(self, roll):
        """Test that FATE dice are reasonably distributed"""
        # Roll many times and check that average is near 0
        results = [roll("4dF")["final"] for _ in range(100)]
        avg = sum(results) / len(results)
        # Average should be close to 0 (allow some variance)
        assert -1 <= avg <= 1


class TestFateEdgeCases:
    """Test edge cases for FATE dice"""

    def test_fate_zero_modifier(self, roll):
        """Test FATE with zero modifier"""
        result = roll("4dF+0")
        assert result["ok"] is True
        assert -4 <= result["final"] <= 4

    def test_large_fate_pool(self, roll):
        """Test rolling many FATE dice"""
        result = roll("10dF")
        assert result["ok"] is True
        assert -10 <= result["final"] <= 10

    def test_fate_case_insensitive(self, roll):
        """Test that dF works regardless of case"""
        result1 = roll("4dF")
        result2 = roll("4df")
        # Both should work
        assert result1["ok"] is True
        assert result2["ok"] is True


class TestFateInExpressions:
    """Test FATE dice in complex expressions"""

    def test_fate_with_arithmetic(self, roll):
        """Test FATE in arithmetic expression"""
        result = roll("4dF+2+1")
        assert result["ok"] is True

    def test_fate_multiplication(self, roll):
        """Test FATE with multiplication"""
        result = roll("(4dF+2)*2")
        assert result["ok"] is True

    def test_multiple_fate_rolls(self, roll):
        """Test multiple FATE rolls in one expression"""
        result = roll("4dF+4dF")
        assert result["ok"] is True
        assert -8 <= result["final"] <= 8
