# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude skill that provides true random dice rolling for tabletop RPGs using cryptographically secure random number generation (CSPRNG). The core implementation is a single Python script ([dice_roller.py](src/scripts/dice_roller.py)) that parses dice notation and generates verifiable random results.

## Development Commands

### Testing the Dice Roller

```bash
# Test basic dice expressions
python3 src/scripts/dice_roller.py "3d6"
python3 src/scripts/dice_roller.py "2d20kh1+5"
python3 src/scripts/dice_roller.py "4d6kh3"

# Test complex expressions
python3 src/scripts/dice_roller.py "(4d6kh3)+(2d8)+3"
python3 src/scripts/dice_roller.py "10d10>=7"
python3 src/scripts/dice_roller.py "4dF+3"
```

The script outputs structured JSON with complete roll information.

### Building the Skill Package

```bash
# Build the skill zip file for distribution
python3 build.py

# The output will be in dist/ttrpg-dice-roller.zip
```

### Future Testing (Once Implemented)

See [TESTING_AND_DEPLOY_PLAN.md](plans/TESTING_AND_DEPLOY_PLAN.md) for the planned test infrastructure:

```bash
# Run all tests (once test suite is created)
uv run pytest

# Run with coverage
uv run pytest --cov=src/scripts --cov-report=html

# Run specific test file
uv run pytest tests/test_parser.py

# Run linter
uv run ruff check src/
```

## Architecture

### Core Components

The implementation uses a recursive descent parser with proper operator precedence:

1. **Tokenization** ([dice_roller.py:814](src/scripts/dice_roller.py)) - Regex-based lexical analysis
2. **Parsing** - Recursive descent parser that builds an abstract syntax tree
3. **Evaluation** - AST traversal with CSPRNG integration for die rolls
4. **Tracing** - Complete roll history for transparency

### Key Classes

- **`DiceParser`** - Handles tokenization and parsing of dice notation expressions
- **`DiceEvaluator`** - Evaluates parsed expressions and generates random results
- **`DieRoll`** - Dataclass representing a single die roll with history (rerolls, explosions)
- **`DiceTrace`** - Dataclass containing the complete trace of a dice term evaluation

### Random Number Generation

The roller uses **cryptographically secure random number generation** (CSPRNG) via Python's `secrets` module with **rejection sampling** to eliminate modulo bias:

```python
# Ensures true randomness with no statistical bias
def roll_die(sides):
    max_value = (1 << (bytes_needed * 8))
    bound = (max_value // sides) * sides

    while True:
        value = secrets.token_bytes(bytes_needed)
        if value < bound:
            return (value % sides) + 1
```

### Safety Limits

Hard-coded limits prevent abuse and infinite loops:

- `MAX_DICE = 1000` - Maximum dice per term
- `MAX_SIDES = 1_000_000_000` - Maximum sides per die
- `MAX_EXPLOSIONS = 100` - Maximum explosion iterations
- `MAX_REROLLS = 10000` - Maximum reroll iterations
- `MAX_RECURSION = 32` - Maximum parentheses nesting depth

## Output Format

The dice roller returns structured JSON with two possible output types:

### Standard Roll (Sum)
```json
{
  "ok": true,
  "final": 15,
  "type": "sum",
  "trace": [...],
  "rng": {"source": "CSPRNG", "method": "rejectionSampling"},
  "limits": {...},
  "version": "dice-1.0.0"
}
```

### Success Counting
```json
{
  "ok": true,
  "final": 7,
  "type": "success_count",
  "trace": [...],
  "rng": {...}
}
```

### Error Response
```json
{
  "ok": false,
  "error": {
    "type": "ParseError",
    "message": "Expected number after 'kh'",
    "position": 4,
    "input": "4d6kh"
  }
}
```

## Error Handling

Four error types with detailed position information:

- **`ParseError`** - Invalid syntax (includes position and context)
- **`SemanticError`** - Invalid dice rules (e.g., keep more dice than rolled)
- **`LimitError`** - Safety limit exceeded
- **`RuntimeError`** - Unexpected execution error (division by zero, etc.)

## Dice Notation Support

The parser supports extensive dice notation:

- **Basic**: `3d6`, `d20`, `d%`, `dF` (FATE dice)
- **Keep/Drop**: `kh3`, `kl1`, `dh2`, `dl1`
- **Rerolls**: `r1`, `ro1`, `r<2`, `r>=5`
- **Explosions**: `!`, `!p`, `!!`, `!>=10`
- **Success Counting**: `>=7`, `<=3`, `=5`
- **Arithmetic**: `+`, `-`, `*`, `/`, `()`
- **Display**: `sa` (sort ascending), `sd` (sort descending)

## Known Limitations

- **Comparator + Explosion**: Cannot combine success counting with explosions in a single expression (e.g., `10d10!>=7` will sum explosions, not count successes). Workaround: Roll separately.
- **Multiple Comparators**: Only one comparator per dice term
- **No Macro Variables**: No support for saved variables or macros
- **No Conditional Logic**: No if/then branching

## File Structure

```
src/
├── SKILL.md              # Skill documentation for Claude (how to use the skill)
└── scripts/
    └── dice_roller.py    # Core implementation (~814 lines)
```

When packaged as a skill, the entire `src/` directory is zipped and uploaded to Claude.

## Development Workflow

1. **Make changes** to [dice_roller.py](src/scripts/dice_roller.py)
2. **Test manually** with various dice expressions
3. **Update** [SKILL.md](src/SKILL.md) if notation changes
4. **Update** [README.md](README.md) if user-facing features change
5. **Build package** with `python3 build.py`

## Future Enhancements

See [TESTING_AND_DEPLOY_PLAN.md](plans/TESTING_AND_DEPLOY_PLAN.md) for planned improvements:

- UV package manager for dependency management
- Comprehensive pytest test suite
- GitHub Actions CI/CD for automated testing and releases
- Multi-version Python testing (3.7-3.12)
- Ruff linting for code quality
