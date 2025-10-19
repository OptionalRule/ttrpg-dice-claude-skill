"""Tests for error handling and validation"""
import pytest


class TestParseErrors:
    """Test parse error detection and messages"""

    def test_invalid_syntax(self, roll):
        """Test that invalid syntax returns an error"""
        result = roll("invalid")
        assert result["ok"] is False
        assert result["error"]["type"] == "ParseError"

    def test_incomplete_modifier(self, roll):
        """Test incomplete modifier (e.g., 'kh' without number)"""
        result = roll("4d6kh")
        assert result["ok"] is False
        assert result["error"]["type"] == "ParseError"
        assert "position" in result["error"]

    def test_malformed_dice_notation(self, roll):
        """Test malformed dice notation"""
        result = roll("d")
        assert result["ok"] is False

    def test_missing_operand(self, roll):
        """Test missing operand"""
        result = roll("3d6+")
        assert result["ok"] is False

    def test_unmatched_parenthesis(self, roll):
        """Test unmatched parenthesis"""
        result = roll("(2d6+3")
        assert result["ok"] is False

    def test_empty_parentheses(self, roll):
        """Test empty parentheses"""
        result = roll("()")
        assert result["ok"] is False

    def test_error_position_information(self, roll):
        """Test that errors include position information"""
        result = roll("4d6kh")
        assert result["ok"] is False
        assert "position" in result["error"]
        assert "input" in result["error"]
        assert result["error"]["input"] == "4d6kh"


class TestSemanticErrors:
    """Test semantic errors (invalid dice rules)"""

    def test_keep_more_than_rolled(self, roll):
        """Test trying to keep more dice than rolled"""
        result = roll("3d6kh5")
        assert result["ok"] is False
        assert result["error"]["type"] == "SemanticError"

    def test_drop_more_than_rolled(self, roll):
        """Test trying to drop more dice than rolled"""
        result = roll("3d6dl5")
        assert result["ok"] is False

    def test_zero_dice(self, roll):
        """Test rolling zero dice"""
        result = roll("0d6")
        assert result["ok"] is False

    def test_negative_dice(self, roll):
        """Test rolling negative dice"""
        result = roll("-1d6")
        # This might parse as subtraction, so check the behavior
        assert result["ok"] is False or result["final"] < 0

    def test_zero_sided_die(self, roll):
        """Test zero-sided die"""
        result = roll("1d0")
        assert result["ok"] is False


class TestLimitErrors:
    """Test safety limit enforcement"""

    def test_too_many_dice(self, roll):
        """Test exceeding maximum dice limit"""
        result = roll("10000d6")
        assert result["ok"] is False
        assert result["error"]["type"] == "LimitError"

    def test_die_too_large(self, roll):
        """Test die with too many sides"""
        result = roll("1d9999999999")
        assert result["ok"] is False
        assert result["error"]["type"] == "LimitError"

    def test_explosion_limit(self, roll):
        """Test that explosions are limited"""
        # Note: This test might pass if the explosion limit prevents infinite loops
        result = roll("1d1!")
        # d1 always rolls 1, which would trigger infinite explosions
        # The implementation should catch this and either error or limit it
        assert result["ok"] is True or result["error"]["type"] == "LimitError"


class TestDivisionByZero:
    """Test division by zero handling"""

    def test_divide_by_zero(self, roll):
        """Test division by zero"""
        result = roll("6d6/0")
        assert result["ok"] is False
        assert result["error"]["type"] in ["RuntimeError", "DiceError"]


class TestErrorMessages:
    """Test that error messages are helpful"""

    def test_error_message_clarity(self, roll):
        """Test that error messages are clear and helpful"""
        result = roll("4d6kh")
        assert result["ok"] is False
        assert "message" in result["error"]
        assert len(result["error"]["message"]) > 0

    def test_error_type_present(self, roll):
        """Test that error type is always present"""
        test_cases = ["invalid", "4d6kh", "10000d6", "()"]
        for expr in test_cases:
            result = roll(expr)
            if not result["ok"]:
                assert "type" in result["error"]
                assert result["error"]["type"] in [
                    "ParseError",
                    "SemanticError",
                    "LimitError",
                    "RuntimeError"
                ]


class TestRecoveryFromErrors:
    """Test that errors don't affect subsequent rolls"""

    def test_error_recovery(self, roll):
        """Test that a valid roll works after an error"""
        # First, cause an error
        result1 = roll("invalid")
        assert result1["ok"] is False

        # Then verify a valid roll still works
        result2 = roll("3d6")
        assert result2["ok"] is True
        assert 3 <= result2["final"] <= 18

    def test_multiple_errors(self, roll):
        """Test handling multiple errors in sequence"""
        errors = [
            roll("invalid"),
            roll("4d6kh"),
            roll("()"),
        ]
        for error in errors:
            assert error["ok"] is False

        # Verify system still works
        result = roll("2d6")
        assert result["ok"] is True
