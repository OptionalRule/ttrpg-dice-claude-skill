"""Tests for success counting (threshold comparisons)"""
import pytest


class TestGreaterThanOrEqual:
    """Test >= success counting"""

    def test_basic_greater_equal(self, roll):
        """Test basic >= success counting"""
        result = roll("10d10>=7")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        # Count how many dice are actually >= 7
        successes = sum(1 for r in result["trace"][0]["rolls"] if r["value"] >= 7)
        assert result["final"] == successes

    def test_all_successes(self, roll):
        """Test when all dice succeed"""
        result = roll("5d6>=1")
        assert result["final"] == 5  # All dice should be >= 1

    def test_no_successes(self, roll):
        """Test when no dice succeed"""
        result = roll("5d6>=7")
        # Might be 0 successes (6-sided dice can't roll 7+)
        assert result["final"] == 0

    def test_threshold_metadata(self, roll):
        """Test that threshold is included in trace"""
        result = roll("8d10>=8")
        assert "threshold" in result["trace"][0]
        assert result["trace"][0]["threshold"] == ">=8"

    def test_success_marks(self, roll):
        """Test that individual rolls are marked as success/fail"""
        result = roll("10d6>=4")
        for r in result["trace"][0]["rolls"]:
            assert "success" in r
            expected_success = r["value"] >= 4
            assert r["success"] == expected_success


class TestGreaterThan:
    """Test > success counting"""

    def test_basic_greater_than(self, roll):
        """Test basic > success counting"""
        result = roll("10d10>5")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        successes = sum(1 for r in result["trace"][0]["rolls"] if r["value"] > 5)
        assert result["final"] == successes


class TestLessThanOrEqual:
    """Test <= success counting"""

    def test_basic_less_equal(self, roll):
        """Test basic <= success counting"""
        result = roll("10d6<=3")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        successes = sum(1 for r in result["trace"][0]["rolls"] if r["value"] <= 3)
        assert result["final"] == successes


class TestLessThan:
    """Test < success counting"""

    def test_basic_less_than(self, roll):
        """Test basic < success counting"""
        result = roll("10d6<4")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        successes = sum(1 for r in result["trace"][0]["rolls"] if r["value"] < 4)
        assert result["final"] == successes


class TestEquals:
    """Test = (exact match) success counting"""

    def test_basic_equals(self, roll):
        """Test basic = success counting"""
        result = roll("20d6=6")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        successes = sum(1 for r in result["trace"][0]["rolls"] if r["value"] == 6)
        assert result["final"] == successes

    def test_count_specific_number(self, roll):
        """Test counting a specific number"""
        result = roll("10d10=5")
        # Should count how many 5s were rolled
        assert result["final"] >= 0
        assert result["type"] == "success_count"


class TestSuccessCountingWithModifiers:
    """Test success counting combined with other modifiers"""

    def test_success_with_keep_highest(self, roll):
        """Test success counting with keep highest"""
        result = roll("10d10kh5>=7")
        assert result["ok"] is True
        # Should only count successes in the kept dice
        assert result["type"] == "success_count"

    def test_success_count_metadata(self, roll):
        """Test that successes field is present"""
        result = roll("10d6>=4")
        assert "successes" in result["trace"][0]
        assert result["trace"][0]["successes"] == result["final"]


class TestStorytellerStyle:
    """Test Storyteller/World of Darkness style dice pools"""

    def test_storyteller_difficulty_8(self, roll):
        """Test typical Storyteller roll (difficulty 8)"""
        result = roll("8d10>=8")
        assert result["ok"] is True
        assert result["type"] == "success_count"
        assert 0 <= result["final"] <= 8

    def test_storyteller_difficulty_6(self, roll):
        """Test Storyteller roll with difficulty 6"""
        result = roll("10d10>=6")
        assert result["ok"] is True
        assert result["type"] == "success_count"
