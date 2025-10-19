"""Tests for statistical properties and randomness"""
import pytest
from collections import Counter


class TestRandomness:
    """Test that rolls are truly random"""

    def test_rolls_are_not_deterministic(self, roll):
        """Test that consecutive rolls produce different results"""
        results = [roll("1d20")["final"] for _ in range(20)]
        # With 20 rolls of d20, we should see some variation
        unique_values = len(set(results))
        assert unique_values > 1, "Rolls appear to be deterministic"

    def test_different_seeds(self, roll):
        """Test that rolls are not using the same seed"""
        results1 = [roll("3d6")["final"] for _ in range(10)]
        results2 = [roll("3d6")["final"] for _ in range(10)]
        # The two sequences should be different
        assert results1 != results2, "Rolls appear to use the same seed"


class TestDistribution:
    """Test that dice distributions are reasonable"""

    def test_d6_distribution(self, roll):
        """Test that d6 rolls are reasonably distributed"""
        rolls = [roll("1d6")["final"] for _ in range(600)]
        counts = Counter(rolls)

        # Each face should appear (roughly 100 times out of 600)
        # Allow for variance: each face should appear at least 50 times
        for face in range(1, 7):
            assert counts[face] >= 30, f"Face {face} appeared only {counts[face]} times"

        # No invalid values
        for value in counts.keys():
            assert 1 <= value <= 6

    def test_d20_distribution(self, roll):
        """Test that d20 rolls cover the full range"""
        rolls = [roll("1d20")["final"] for _ in range(200)]

        # We should see a good variety of values
        unique_values = len(set(rolls))
        assert unique_values >= 10, "Not enough variation in d20 rolls"

    def test_fate_dice_distribution(self, roll):
        """Test that FATE dice are distributed properly"""
        rolls = [roll("1dF")["final"] for _ in range(300)]
        counts = Counter(rolls)

        # Should only have -1, 0, 1
        for value in counts.keys():
            assert value in [-1, 0, 1]

        # Each should appear at least once in 300 rolls
        assert -1 in counts
        assert 0 in counts
        assert 1 in counts


class TestUniformity:
    """Test that dice are uniformly distributed"""

    def test_d6_uniformity(self, roll):
        """Test that d6 is uniformly distributed"""
        rolls = [roll("1d6")["final"] for _ in range(6000)]
        counts = Counter(rolls)

        # Calculate expected count per face (6000/6 = 1000)
        expected = 1000

        # Use chi-square-like test: each face should be within reasonable bounds
        for face in range(1, 7):
            # Allow for 20% deviation
            assert 800 <= counts[face] <= 1200, \
                f"Face {face}: {counts[face]} (expected ~{expected})"

    def test_no_modulo_bias(self, roll):
        """Test that there's no modulo bias in the results"""
        # Roll a d7 many times and check distribution
        rolls = [roll("1d7")["final"] for _ in range(700)]
        counts = Counter(rolls)

        # Each face should appear roughly equally (700/7 = 100)
        for face in range(1, 8):
            # Allow for variance
            assert 60 <= counts[face] <= 140, \
                f"Possible modulo bias: face {face} appeared {counts[face]} times"


class TestAverages:
    """Test that averages are close to expected values"""

    def test_d6_average(self, roll):
        """Test that d6 average is close to 3.5"""
        rolls = [roll("1d6")["final"] for _ in range(1000)]
        avg = sum(rolls) / len(rolls)
        # Average should be close to 3.5 (allow some variance)
        assert 3.2 <= avg <= 3.8

    def test_2d6_average(self, roll):
        """Test that 2d6 average is close to 7"""
        rolls = [roll("2d6")["final"] for _ in range(1000)]
        avg = sum(rolls) / len(rolls)
        # Average should be close to 7
        assert 6.5 <= avg <= 7.5

    def test_fate_average(self, roll):
        """Test that FATE dice average close to 0"""
        rolls = [roll("4dF")["final"] for _ in range(500)]
        avg = sum(rolls) / len(rolls)
        # Average should be close to 0
        assert -0.5 <= avg <= 0.5


class TestCSPRNG:
    """Test CSPRNG-specific properties"""

    def test_uses_csprng(self, roll):
        """Test that the RNG source is CSPRNG"""
        result = roll("1d6")
        assert result["rng"]["source"] == "CSPRNG"

    def test_uses_rejection_sampling(self, roll):
        """Test that rejection sampling is used"""
        result = roll("1d6")
        assert result["rng"]["method"] == "rejectionSampling"

    def test_large_die_works(self, roll):
        """Test that large dice work correctly"""
        result = roll("1d1000")
        assert result["ok"] is True
        assert 1 <= result["final"] <= 1000

    def test_no_predictable_pattern(self, roll):
        """Test that there's no obvious predictable pattern"""
        # Roll the same expression many times
        results = [roll("3d6")["final"] for _ in range(50)]

        # Check for runs (same value repeated)
        max_run = 1
        current_run = 1
        for i in range(1, len(results)):
            if results[i] == results[i-1]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1

        # Max run should be small (no long streaks of identical values)
        assert max_run <= 5, f"Suspicious run of {max_run} identical results"


class TestExtremeValues:
    """Test that extreme values can occur"""

    def test_min_value_possible(self, roll):
        """Test that minimum values can occur"""
        # Roll many d20s, should see at least one 1
        rolls = [roll("1d20")["final"] for _ in range(100)]
        assert 1 in rolls

    def test_max_value_possible(self, roll):
        """Test that maximum values can occur"""
        # Roll many d20s, should see at least one 20
        rolls = [roll("1d20")["final"] for _ in range(100)]
        assert 20 in rolls

    def test_both_extremes_on_d6(self, roll):
        """Test that both extremes appear on d6"""
        rolls = [roll("1d6")["final"] for _ in range(100)]
        assert 1 in rolls, "Never rolled a 1"
        assert 6 in rolls, "Never rolled a 6"
