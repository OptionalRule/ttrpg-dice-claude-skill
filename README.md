# TTRPG Dice Roller - Claude Skill

A Claude skill that enables true random dice rolling for tabletop RPGs using cryptographically secure random number generation.

## What Is This?

This is a **skill for Claude** that lets you roll dice using standard tabletop RPG notation. When you upload this skill to Claude, you can simply say things like:

- "Roll 4d6, keep the highest 3" (for D&D ability scores)
- "Roll 2d20 with advantage plus 5" (for D&D attacks)
- "Roll 10d10, count successes of 7 or higher" (for Storyteller games)
- "Roll 4dF+3" (for FATE)

Claude will understand your request and return truly random results with complete transparency about what was rolled.

**Key Features:**
- 🎲 Cryptographically secure randomness (not pseudo-random)
- 🎯 Supports D&D, Pathfinder, Storyteller, Savage Worlds, FATE, and more
- 📊 Shows you all the dice that were rolled, not just the final number
- 🔢 Handles complex expressions with keep/drop, rerolls, explosions, and modifiers
- 🛡️ Safe limits prevent infinite loops

## How to Use

### Download the Skill

**Latest Release:** Download `ttrpg-dice-roller.zip` from the [Releases](https://github.com/yourusername/ttrpg-dice-roller/releases) page.

### Install in Claude

1. Open Claude (web, desktop, or mobile)
2. Go to the Skills section
3. Upload the `ttrpg-dice-roller.zip` file
4. That's it! Claude will now automatically use this skill when you ask to roll dice

For help with uploading skills, visit [Claude Support](https://support.claude.com).

### Using the Skill

Once installed, just ask Claude naturally:

```
You: "Roll 4d6 and keep the highest 3 for my character's Strength score"

Claude: I'll roll 4d6 and keep the highest 3 dice.

Rolling 4d6kh3...
Rolled: [6, 5, 4, 2]
Kept: [6, 5, 4]
Result: 15
```

Claude understands standard RPG dice notation, so you can use expressions like:
- `3d6+5` - Roll 3 six-sided dice and add 5
- `2d20kh1` - Roll 2 twenty-sided dice, keep the highest
- `10d10>=7` - Roll 10 ten-sided dice, count how many are 7 or higher
- `4dF+2` - Roll 4 FATE dice and add 2

## Building from Source

If you want to build the skill package yourself:

### Prerequisites
- Python 3.7 or higher
- Git

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/ttrpg-dice-roller.git
cd ttrpg-dice-roller

# Build the skill package
python3 build.py

# The skill package will be created at dist/ttrpg-dice-roller.zip
```

The build script will create a properly packaged skill zip file ready to upload to Claude.

---

## For Developers: Technical Details

**The information below is for developers who want to understand the implementation, contribute to the project, or integrate the dice roller into other applications. You don't need to read this section to use the skill in Claude.**

### Project Structure

```
ttrpg-dice-roller/
├── src/
│   ├── SKILL.md                 # Claude skill documentation
│   └── scripts/
│       └── dice_roller.py       # Core implementation (~800 lines)
├── README.md                    # This file
├── LICENSE.txt                  # MIT License
└── build.py                     # Build script (generates zip)
```

### Testing the Dice Roller Directly

You can test the dice roller script directly without Claude:

```bash
# From the project root
python3 src/scripts/dice_roller.py "4d6kh3"
python3 src/scripts/dice_roller.py "2d20kh1+5"
python3 src/scripts/dice_roller.py "10d10>=7"
```

The script outputs structured JSON with complete roll information.

### Command-Line Examples

#### D&D / Pathfinder

```bash
# Ability score generation (4d6, drop lowest)
python3 src/scripts/dice_roller.py "4d6kh3"

# Attack roll with advantage (keep highest)
python3 src/scripts/dice_roller.py "2d20kh1+5"

# Attack roll with disadvantage (keep lowest)
python3 src/scripts/dice_roller.py "2d20kl1+3"

# Critical hit damage
python3 src/scripts/dice_roller.py "4d8+2d6+4"
```

#### Storyteller / World of Darkness

```bash
# Dice pool counting successes (threshold ≥8)
python3 src/scripts/dice_roller.py "10d10>=8"

# Exploding dice pool
python3 src/scripts/dice_roller.py "10d10!"
```

#### Savage Worlds

```bash
# Standard exploding die
python3 src/scripts/dice_roller.py "1d6!"

# Exploding with penetration (ace minus 1)
python3 src/scripts/dice_roller.py "1d6!p"
```

#### FATE / Fudge

```bash
# Standard FATE roll (4dF)
python3 src/scripts/dice_roller.py "4dF"

# FATE with skill rating
python3 src/scripts/dice_roller.py "4dF+3"
```

#### Complex Expressions

```bash
# Multiple dice pools with arithmetic
python3 src/scripts/dice_roller.py "(4d6kh3)+(2d8)+3"

# Reroll 1s once, keep highest 3
python3 src/scripts/dice_roller.py "4d6ro1kh3"

# Percentile roll
python3 src/scripts/dice_roller.py "d%"
```

## Dice Notation Reference

### Basic Dice

| Notation | Description | Example |
|----------|-------------|---------|
| `NdM` | Roll N dice with M sides | `3d6` = roll 3 six-sided dice |
| `dM` | Roll a single M-sided die | `d20` = roll one twenty-sided die |
| `d%` or `d00` | Percentile dice (d100) | `d%` = roll 1-100 |
| `dF` | FATE/Fudge dice (-1, 0, +1) | `4dF` = roll 4 FATE dice |

### Modifiers

#### Keep/Drop
| Notation | Description | Example |
|----------|-------------|---------|
| `khN` | Keep highest N dice | `4d6kh3` = roll 4d6, keep highest 3 |
| `klN` | Keep lowest N dice | `4d6kl1` = roll 4d6, keep lowest 1 |
| `dhN` | Drop highest N dice | `5d6dh2` = roll 5d6, drop highest 2 |
| `dlN` | Drop lowest N dice | `4d6dl1` = roll 4d6, drop lowest 1 |

#### Rerolls
| Notation | Description | Example |
|----------|-------------|---------|
| `rN` | Reroll value N indefinitely | `8d6r1` = reroll all 1s |
| `roN` | Reroll value N once only | `8d6ro1` = reroll 1s once |
| `r<N` | Reroll values less than N | `4d6r<2` = reroll 1s |
| `r<=N` | Reroll values ≤ N | `4d6r<=2` = reroll 1s and 2s |
| `r>N` | Reroll values greater than N | `4d6r>5` = reroll 6s |
| `r>=N` | Reroll values ≥ N | `4d6r>=5` = reroll 5s and 6s |

#### Explosions (Ace/Open-Ended)
| Notation | Description | Example |
|----------|-------------|---------|
| `!` | Explode on max value | `3d6!` = add extra die when rolling 6 |
| `!p` | Penetrating explosion (-1) | `1d6!p` = explode but subtract 1 |
| `!!` | Compound explosion (same die) | `3d6!!` = add to same die total |
| `!>=N` | Explode on value ≥ N | `3d6!>=5` = explode on 5 or 6 |
| `!<N` | Explode on value < N | `3d6!<3` = explode on 1 or 2 |

#### Success Counting
| Notation | Description | Example |
|----------|-------------|---------|
| `>=N` | Count successes ≥ N | `10d10>=7` = count dice ≥7 |
| `<=N` | Count successes ≤ N | `10d10<=3` = count dice ≤3 |
| `=N` | Count exact matches | `10d6=6` = count sixes |
| `>N` | Count successes > N | `8d10>8` = count dice >8 |
| `<N` | Count successes < N | `8d10<3` = count dice <3 |

#### Arithmetic
| Notation | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `3d6+5` = roll 3d6 and add 5 |
| `-` | Subtraction | `2d8-2` = roll 2d8 and subtract 2 |
| `*` | Multiplication | `2d4*3` = roll 2d4 and multiply by 3 |
| `/` | Division | `4d6/2` = roll 4d6 and divide by 2 |
| `()` | Grouping | `(4d6kh3)+2` = group operations |

#### Display
| Notation | Description | Example |
|----------|-------------|---------|
| `sa` | Sort ascending | `4d6sa` = display sorted low to high |
| `sd` | Sort descending | `4d6sd` = display sorted high to low |

## Output Format

The dice roller returns structured JSON with complete roll information:

### Standard Roll (Sum)

```json
{
  "ok": true,
  "final": 15,
  "type": "sum",
  "trace": [
    {
      "term": "4d6kh3",
      "rolls": [
        {"value": 6},
        {"value": 5},
        {"value": 4},
        {"value": 2}
      ],
      "keptValues": [6, 5, 4],
      "sum": 15
    }
  ],
  "rng": {
    "source": "CSPRNG",
    "method": "rejectionSampling"
  },
  "limits": {
    "maxDice": 1000,
    "maxExplosions": 100
  },
  "version": "dice-1.0.0"
}
```

### Success Counting

```json
{
  "ok": true,
  "final": 7,
  "type": "success_count",
  "trace": [
    {
      "term": "10d10>=7",
      "rolls": [
        {"value": 9, "success": true},
        {"value": 6, "success": false},
        {"value": 8, "success": true}
      ],
      "threshold": ">=7",
      "successes": 7
    }
  ],
  "rng": {
    "source": "CSPRNG",
    "method": "rejectionSampling"
  }
}
```

### With Explosions

```json
{
  "ok": true,
  "final": 28,
  "type": "sum",
  "trace": [
    {
      "term": "3d6!",
      "rolls": [
        {"value": 4},
        {
          "value": 6,
          "explodes": [
            {"value": 6},
            {"value": 6},
            {"value": 3}
          ]
        },
        {"value": 3}
      ],
      "sum": 28
    }
  ]
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

## Technical Details

### Random Number Generation

The roller uses **cryptographically secure random number generation** (CSPRNG) via Python's `secrets` module, with **rejection sampling** to eliminate modulo bias:

```python
# Pseudocode for unbiased die rolling
def roll_die(sides):
    max_value = (1 << (bytes_needed * 8))
    bound = (max_value // sides) * sides
    
    while True:
        value = secrets.token_bytes(bytes_needed)
        if value < bound:
            return (value % sides) + 1
```

This ensures:
- **True randomness** using OS-level entropy
- **No modulo bias** that would favor certain outcomes
- **Cryptographic security** suitable for high-stakes games
- **Full transparency** with traceable results

### Safety Limits

| Parameter | Default | Purpose |
|-----------|---------|---------|
| Max dice per term | 1,000 | Prevent memory exhaustion |
| Max sides per die | 1,000,000,000 | Reasonable upper bound |
| Max explosions | 100 | Prevent infinite loops |
| Max rerolls | 10,000 | Prevent infinite loops |
| Max recursion depth | 32 | Limit parentheses nesting |

### Parser Architecture

The implementation uses a **recursive descent parser** with proper operator precedence:

1. **Tokenization** - Regex-based lexical analysis
2. **Parsing** - Recursive descent with precedence climbing
3. **Evaluation** - AST traversal with RNG integration
4. **Tracing** - Complete roll history for transparency

### Error Handling

Four error types with detailed messages:

- **ParseError** - Invalid syntax (position + context)
- **SemanticError** - Invalid dice rules
- **LimitError** - Safety limit exceeded
- **RuntimeError** - Unexpected execution error

## Development

### Running Tests

```bash
# Test basic rolls
python3 src/scripts/dice_roller.py "3d6"
python3 src/scripts/dice_roller.py "d20+5"

# Test modifiers
python3 src/scripts/dice_roller.py "4d6kh3"
python3 src/scripts/dice_roller.py "8d6ro1"
python3 src/scripts/dice_roller.py "3d6!"

# Test success counting
python3 src/scripts/dice_roller.py "10d10>=7"

# Test complex expressions
python3 src/scripts/dice_roller.py "(4d6kh3)+(3d8)+5"

# Test FATE dice
python3 src/scripts/dice_roller.py "4dF+2"

# Test error handling
python3 src/scripts/dice_roller.py "4d6kh"    # Should error: missing number
python3 src/scripts/dice_roller.py "invalid"  # Should error: invalid syntax
```

### Statistical Validation

To verify randomness and uniformity:

```bash
# Roll many d6s and check distribution
for i in {1..1000}; do
    python3 src/scripts/dice_roller.py "1d6" | jq -r '.final'
done | sort -n | uniq -c

# Expected: roughly equal counts for 1-6
```

### Extending the Skill

To add new features:

1. Update the parser grammar in `DiceParser` class in `src/scripts/dice_roller.py`
2. Add evaluation logic in `DiceEvaluator` class
3. Update `src/SKILL.md` with new notation documentation
4. Add examples and tests
5. Update this README
6. Rebuild the skill package with `python3 build.py`

## Use Cases

### Game Masters
- Quick rolls for NPCs and monsters
- Transparent results for player trust
- Complex damage calculations
- Random encounters and loot

### Players
- Character creation (ability scores)
- Attack rolls with advantage/disadvantage
- Skill checks with modifiers
- Damage calculations

### Developers
- Integration into VTT software
- Discord bots for RPG servers
- Game design and balance testing
- Statistical analysis of game mechanics

### Solo Players
- Oracle rolls for solo RPGs
- Procedural generation
- Random tables and charts
- Automated bookkeeping

## Comparison with Other Dice Rollers

| Feature | This Skill | Roll20 | Foundry VTT | Physical Dice |
|---------|-----------|--------|-------------|---------------|
| **True Random** | ✅ CSPRNG | ❌ PRNG | ❌ PRNG | ✅ Physical |
| **No Modulo Bias** | ✅ Rejection sampling | ❌ Simple modulo | ❌ Simple modulo | ✅ N/A |
| **Full Trace** | ✅ Complete history | ✅ Partial | ✅ Partial | ❌ None |
| **Offline Use** | ✅ Yes | ❌ Requires server | ❌ Requires server | ✅ Yes |
| **Verifiable** | ✅ Transparent code | ❌ Closed source | ⚠️ Some modules | ❌ Trust-based |
| **Complex Notation** | ✅ Full support | ✅ Yes | ✅ Yes | ❌ Manual |

## Limitations

- **Comparator + Explosion**: Cannot combine success counting with explosions in a single expression (e.g., `10d10!>=7` will sum explosions, not count successes). Workaround: Roll separately.
- **Multiple Comparators**: Only one comparator per dice term
- **Macro Variables**: No support for saved variables or macros
- **Conditional Logic**: No if/then branching

## Roadmap

Future enhancements:

- [ ] Custom dice types (d66, deck of cards)
- [ ] Macro variables (`STR=4d6kh3`)
- [ ] Conditional rolls (`if/then` logic)
- [ ] Statistical analysis mode
- [ ] Seeded deterministic mode for replay
- [ ] Web interface for testing

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Follow PEP 8 style for Python code
- Add tests for new features
- Update documentation (SKILL.md and README.md)
- Maintain backward compatibility
- Include examples for new notation

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

## Acknowledgments

- Based on the Product Requirements Document by Scott Turnbull
- Inspired by Roll20, Foundry VTT, and AnyDice
- Built for the Claude AI assistant ecosystem
- Special thanks to the TTRPG community for standardizing dice notation

## Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Claude Support**: Visit https://support.claude.com for skill installation help

## References

- [Dice Notation Standard](https://en.wikipedia.org/wiki/Dice_notation) - Background on notation
- [Python secrets module](https://docs.python.org/3/library/secrets.html) - CSPRNG documentation
- [Rejection Sampling](https://en.wikipedia.org/wiki/Rejection_sampling) - Unbiased random generation
- [Claude Skills](https://support.claude.com) - How to use skills in Claude

---

**Made with ❤️ for the tabletop RPG community**

Roll on! 🎲

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.