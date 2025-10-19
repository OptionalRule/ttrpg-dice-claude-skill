"""Tests for complex dice expressions"""
import pytest


class TestComplexArithmetic:
    """Test complex arithmetic expressions"""

    def test_order_of_operations(self, roll):
        """Test that order of operations is correct"""
        result = roll("2d1+3d1*2")
        assert result["final"] == 8  # 2 + (3*2), not (2+3)*2

    def test_nested_parentheses(self, roll):
        """Test deeply nested parentheses"""
        result = roll("(((1d1+1)*2)+1)")
        assert result["final"] == 5  # (((1+1)*2)+1) = ((2*2)+1) = (4+1) = 5

    def test_multiple_parentheses_groups(self, roll):
        """Test multiple groups of parentheses"""
        result = roll("(2d1+1)*(3d1-1)")
        assert result["final"] == 6  # (2+1)*(3-1) = 3*2 = 6


class TestRealWorldScenarios:
    """Test realistic RPG scenarios"""

    def test_dnd_ability_score(self, roll):
        """Test D&D ability score generation (4d6, drop lowest)"""
        result = roll("4d6dl1")
        assert result["ok"] is True
        assert 3 <= result["final"] <= 18
        assert len(result["trace"][0]["rolls"]) == 4
        assert len(result["trace"][0]["keptValues"]) == 3

    def test_dnd_advantage(self, roll):
        """Test D&D advantage (roll 2d20, keep highest)"""
        result = roll("2d20kh1")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 20
        assert len(result["trace"][0]["rolls"]) == 2
        assert len(result["trace"][0]["keptValues"]) == 1

    def test_dnd_disadvantage(self, roll):
        """Test D&D disadvantage (roll 2d20, keep lowest)"""
        result = roll("2d20kl1")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 20

    def test_dnd_attack_with_modifier(self, roll):
        """Test D&D attack roll with modifier"""
        result = roll("1d20+5")
        assert result["ok"] is True
        assert 6 <= result["final"] <= 25

    def test_dnd_critical_damage(self, roll):
        """Test D&D critical hit (double dice)"""
        result = roll("4d6+2d4+3")
        assert result["ok"] is True
        # Min: 4+2+3=9, Max: 24+8+3=35
        assert 9 <= result["final"] <= 35

    def test_savage_worlds_exploding_die(self, roll):
        """Test Savage Worlds exploding die"""
        result = roll("1d6!")
        assert result["ok"] is True
        assert result["final"] >= 1

    def test_savage_worlds_skill_check(self, roll):
        """Test Savage Worlds skill + wild die"""
        result = roll("1d8!+1d6!")
        assert result["ok"] is True
        assert result["final"] >= 2


class TestMultipleDiceTypes:
    """Test expressions with multiple different dice types"""

    def test_mixed_dice_sizes(self, roll):
        """Test mixing different die sizes"""
        result = roll("1d4+1d6+1d8+1d10+1d12+1d20")
        assert result["ok"] is True
        # Min: 1+1+1+1+1+1=6, Max: 4+6+8+10+12+20=60
        assert 6 <= result["final"] <= 60

    def test_fate_mixed_with_regular_dice(self, roll):
        """Test FATE dice mixed with regular dice"""
        result = roll("4dF+2d6")
        assert result["ok"] is True
        # Min: -4+2=-2, Max: 4+12=16
        assert -2 <= result["final"] <= 16


class TestComplexModifiers:
    """Test complex modifier combinations"""

    def test_reroll_and_keep(self, roll):
        """Test reroll combined with keep"""
        result = roll("6d6ro1kh3")
        assert result["ok"] is True
        assert len(result["trace"][0]["keptValues"]) == 3
        # All kept values should be >= 2 (rerolled 1s)
        for val in result["trace"][0]["keptValues"]:
            assert val >= 1  # Note: ro1 means reroll 1s once, not guaranteed no 1s

    def test_multiple_modifiers_chain(self, roll):
        """Test chaining multiple modifiers"""
        result = roll("8d6ro<3kh4")
        assert result["ok"] is True

    def test_exploding_keep_highest(self, roll):
        """Test explosions with keep highest"""
        result = roll("6d6!kh3")
        assert result["ok"] is True
        assert len(result["trace"][0]["keptValues"]) == 3


class TestEdgeCaseExpressions:
    """Test edge case expressions"""

    def test_all_constants(self, roll):
        """Test expression with no dice"""
        result = roll("5+3*2")
        assert result["final"] == 11

    def test_single_constant(self, roll):
        """Test single constant value"""
        result = roll("42")
        assert result["final"] == 42

    def test_zero_result(self, roll):
        """Test expression that results in zero"""
        result = roll("0")
        assert result["final"] == 0

    def test_negative_result(self, roll):
        """Test expression with negative result"""
        result = roll("1d1-5")
        assert result["final"] == -4

    def test_very_long_expression(self, roll):
        """Test a very long but valid expression"""
        expr = "+".join(["1d6"] * 10)
        result = roll(expr)
        assert result["ok"] is True
        assert 10 <= result["final"] <= 60
