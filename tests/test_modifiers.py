"""Tests for dice modifiers (keep, drop, reroll, explode)"""
import pytest


class TestKeepHighest:
    """Test keep highest (kh) modifier"""

    def test_keep_highest_basic(self, roll):
        """Test basic keep highest functionality"""
        result = roll("4d6kh3")
        assert result["ok"] is True
        assert len(result["trace"][0]["rolls"]) == 4
        assert len(result["trace"][0]["keptValues"]) == 3

    def test_keep_highest_one(self, roll):
        """Test keeping only the highest die"""
        result = roll("2d20kh1")
        assert result["ok"] is True
        assert len(result["trace"][0]["keptValues"]) == 1
        # The kept value should be >= both original rolls
        all_rolls = [r["value"] for r in result["trace"][0]["rolls"]]
        kept_value = result["trace"][0]["keptValues"][0]
        assert kept_value == max(all_rolls)

    def test_keep_all_dice(self, roll):
        """Test keeping all dice (should be same as no modifier)"""
        result = roll("3d6kh3")
        assert len(result["trace"][0]["keptValues"]) == 3


class TestKeepLowest:
    """Test keep lowest (kl) modifier"""

    def test_keep_lowest_basic(self, roll):
        """Test basic keep lowest functionality"""
        result = roll("4d6kl1")
        assert result["ok"] is True
        assert len(result["trace"][0]["keptValues"]) == 1
        # The kept value should be <= all original rolls
        all_rolls = [r["value"] for r in result["trace"][0]["rolls"]]
        kept_value = result["trace"][0]["keptValues"][0]
        assert kept_value == min(all_rolls)

    def test_keep_lowest_multiple(self, roll):
        """Test keeping multiple lowest dice"""
        result = roll("5d6kl2")
        assert len(result["trace"][0]["keptValues"]) == 2


class TestDropHighest:
    """Test drop highest (dh) modifier"""

    def test_drop_highest_basic(self, roll):
        """Test basic drop highest functionality"""
        result = roll("4d6dh1")
        assert result["ok"] is True
        assert len(result["trace"][0]["rolls"]) == 4
        assert len(result["trace"][0]["keptValues"]) == 3

    def test_drop_highest_equivalent_to_keep_lowest(self, roll):
        """Test that drop highest is equivalent to keep lowest"""
        # 4d1dh1 should give same result as 4d1kl3
        result1 = roll("4d1dh1")
        result2 = roll("4d1kl3")
        assert result1["final"] == result2["final"] == 3


class TestDropLowest:
    """Test drop lowest (dl) modifier"""

    def test_drop_lowest_basic(self, roll):
        """Test basic drop lowest functionality (classic 4d6 drop lowest)"""
        result = roll("4d6dl1")
        assert result["ok"] is True
        assert len(result["trace"][0]["rolls"]) == 4
        assert len(result["trace"][0]["keptValues"]) == 3

    def test_drop_lowest_equivalent_to_keep_highest(self, roll):
        """Test that drop lowest is equivalent to keep highest"""
        result1 = roll("4d1dl1")
        result2 = roll("4d1kh3")
        assert result1["final"] == result2["final"] == 3


class TestRerolls:
    """Test reroll modifiers"""

    def test_reroll_once(self, roll):
        """Test reroll once (ro) modifier"""
        # Using d1 to test mechanics - it won't actually reroll since it's always 1
        result = roll("5d6ro1")
        assert result["ok"] is True
        # Should have some reroll information if any 1s were rolled

    def test_reroll_condition_less_than(self, roll):
        """Test reroll with < condition"""
        result = roll("4d6r<2")
        assert result["ok"] is True
        # All final values should be >= 2
        for r in result["trace"][0]["rolls"]:
            assert r["value"] >= 2


class TestExplosions:
    """Test explosion (exploding dice) modifiers"""

    def test_basic_explosion(self, roll):
        """Test basic explosion (!)"""
        result = roll("3d6!")
        assert result["ok"] is True
        # Check that explosion field exists if any max values were rolled
        for r in result["trace"][0]["rolls"]:
            if r["value"] == 6:
                # If we rolled a 6, it might have explosions
                assert "value" in r

    def test_penetrating_explosion(self, roll):
        """Test penetrating explosion (!p)"""
        result = roll("2d6!p")
        assert result["ok"] is True

    def test_compound_explosion(self, roll):
        """Test compound explosion (!!)"""
        result = roll("2d6!!")
        assert result["ok"] is True

    def test_conditional_explosion(self, roll):
        """Test conditional explosion"""
        result = roll("3d6!>=5")
        assert result["ok"] is True


class TestSorting:
    """Test sorting modifiers"""

    def test_sort_ascending(self, roll):
        """Test sort ascending (sa)"""
        result = roll("5d6sa")
        assert result["ok"] is True
        # Note: sorting is display-only, doesn't affect result

    def test_sort_descending(self, roll):
        """Test sort descending (sd)"""
        result = roll("5d6sd")
        assert result["ok"] is True


class TestCombinedModifiers:
    """Test combinations of modifiers"""

    def test_reroll_then_keep(self, roll):
        """Test reroll once then keep highest"""
        result = roll("4d6ro1kh3")
        assert result["ok"] is True
        assert len(result["trace"][0]["keptValues"]) == 3

    def test_explode_then_keep(self, roll):
        """Test explosion then keep highest"""
        result = roll("4d6!kh3")
        assert result["ok"] is True
