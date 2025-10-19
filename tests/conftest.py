"""Shared test fixtures and utilities"""
import sys
import os

# Add the src/scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'scripts'))

import pytest
from dice_roller import roll_dice, DiceParser, DiceEvaluator, CSPRNG


@pytest.fixture
def parser():
    """Provide a DiceParser instance"""
    def _parser(expression):
        return DiceParser(expression)
    return _parser


@pytest.fixture
def evaluator():
    """Provide a DiceEvaluator instance"""
    return DiceEvaluator()


@pytest.fixture
def roll():
    """Provide the roll_dice function for easy testing"""
    return roll_dice


@pytest.fixture
def rng():
    """Provide the CSPRNG class"""
    return CSPRNG
