# DropDuchy BattleBot

DropDuchy BattleBot is a simple battle simulation and optimization tool designed to find the best battle sequence between two opposing armies. It uses Streamlit for the user interface and a custom battle engine to calculate battle outcomes.

---

## Overview of the Battle Engine

The core logic of DropDuchy BattleBot is implemented in the `battle_engine.py` module. This engine simulates sequential battles between armies composed of different troop types, following a rock-paper-scissors style advantage system.

### Troop Types and Advantage Rules

- **Archers (archi)** have advantage over **Axemen (asce)**
- **Axemen (asce)** have advantage over **Swordsmen (spade)**
- **Swordsmen (spade)** have advantage over **Archers (archi)**

If two armies have the same troop type or are neutral, no advantage is applied.

---

### Key Classes

- **Army**: Represents a group of troops of a certain type with a numeric strength.
- **Stage**: Represents a sequence of armies fighting one after another.

---

### How Battles Are Simulated

1. **Single combat**: Two armies fight based on their troop types and numbers.
   - If allied (same sign of numbers), their forces combine.
   - If enemies, the army with advantage has increased effectiveness.
   - The winning army’s strength is adjusted by specific rules (see `single_combat`).

2. **Sequential battle**: Armies fight one after another in the order given.
   - The result of the first combat fights the next army, and so on.
   - The final surviving army and its strength represent the battle outcome.

---

### Examples

```python
from battle_engine import Army, Stage, single_combat, Battle

# Example 1: Single combat with advantage
archer = Army(10, 'archi')
axeman = Army(-8, 'asce')  # Negative number means enemy

result = single_combat(archer, axeman)
print(result)  # Expected: Archer wins with adjusted strength

# Example 2: Allies combining
archer1 = Army(5, 'archi')
archer2 = Army(3, 'archi')

result = single_combat(archer1, archer2)
print(result)  # Expected: Combined army with 8 archers

# Example 3: Sequential battle
armies = [
    Army(10, 'archi'),
    Army(-5, 'asce'),
    Army(-7, 'spade')
]
stage = Stage(armies)
final_result = Battle(stage)
print(final_result)  # The army surviving after all battles
