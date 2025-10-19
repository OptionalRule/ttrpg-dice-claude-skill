"""Tests for dice notation parsing"""
import pytest


class TestBasicParsing:
    """Test basic dice expression parsing"""

    def test_simple_dice(self, roll):
        """Test simple dice expressions like 3d6"""
        result = roll("3d6")
        assert result["ok"] is True
        assert 3 <= result["final"] <= 18
        assert result["type"] == "sum"
        assert len(result["trace"][0]["rolls"]) == 3

    def test_single_die(self, roll):
        """Test single die notation like d20"""
        result = roll("d20")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 20

    def test_percentile_dice(self, roll):
        """Test percentile dice (d%)"""
        result = roll("d%")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 100

    def test_percentile_dice_d00(self, roll):
        """Test percentile dice (d00)"""
        result = roll("d00")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 100

    def test_d1_always_returns_1(self, roll):
        """Test that d1 always returns 1"""
        for _ in range(10):
            result = roll("1d1")
            assert result["final"] == 1


class TestArithmetic:
    """Test arithmetic operations in dice expressions"""

    def test_addition(self, roll):
        """Test addition modifier"""
        result = roll("1d1+5")
        assert result["final"] == 6

    def test_subtraction(self, roll):
        """Test subtraction modifier"""
        result = roll("1d1-1")
        assert result["final"] == 0

    def test_multiplication(self, roll):
        """Test multiplication"""
        result = roll("2d1*3")
        assert result["final"] == 6

    def test_division(self, roll):
        """Test division"""
        result = roll("6d1/2")
        assert result["final"] == 3

    def test_complex_arithmetic(self, roll):
        """Test complex arithmetic expression"""
        result = roll("2d1+3d1*2")
        assert result["final"] == 8  # 2 + (3*2)


class TestParentheses:
    """Test grouping with parentheses"""

    def test_simple_grouping(self, roll):
        """Test simple parentheses grouping"""
        result = roll("(2d1+1)*2")
        assert result["final"] == 6  # (2+1)*2

    def test_nested_parentheses(self, roll):
        """Test nested parentheses"""
        result = roll("((1d1+1)*2)+1")
        assert result["final"] == 5  # ((1+1)*2)+1

    def test_multiple_groups(self, roll):
        """Test multiple grouped expressions"""
        result = roll("(2d1)+(3d1)")
        assert result["final"] == 5


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_large_number_of_dice(self, roll):
        """Test rolling many dice"""
        result = roll("100d1")
        assert result["final"] == 100
        assert len(result["trace"][0]["rolls"]) == 100

    def test_whitespace_handling(self, roll):
        """Test that whitespace is handled correctly"""
        result1 = roll("3d6+2")
        result2 = roll("  3d6  +  2  ")
        assert result1["ok"] is True
        assert result2["ok"] is True

    def test_zero_modifier(self, roll):
        """Test adding zero"""
        result = roll("3d6+0")
        assert result["ok"] is True
        assert 3 <= result["final"] <= 18
