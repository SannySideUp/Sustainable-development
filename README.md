# 🌍 Sustainable Development Game

A Python-based educational dice game was designed.  
This project demonstrates modular software design, testing, and documentation best practices.

---

## 🧠 Overview

The **Sustainable Development Game** is a command-line Python game that simulates sustainability-related choices using dice mechanics.  
It emphasizes:
- Object-oriented design
- Persistent high score tracking
- Intelligent AI opponent (different difficulty levels)
- Clear module separation and reusability
- Automatically generated documentation and UML diagrams

The Pig Dice Game is a simple but strategic dice game where a human player competes against an AI opponent.

Each player takes turns rolling a six-sided die to accumulate points.
If a player rolls a 1, their turn score resets to 0, and their turn ends immediately.
If they choose to hold, their turn score is added to their total score.
The first player to reach 100 points wins the game.

The AI opponent has six difficulty levels, each with unique strategies and risk profiles, from Noob to Legendary.


## 🧠 Intelligence System

The AI intelligence is implemented in src/intelligence.py
 through the DiceDifficulty class.

Each difficulty level defines:

- How many rolls it will attempt per turn
- How risky its strategy is (chance to keep rolling vs. hold early)
- Whether it plays safe when leading or aggressive when behind
- A per-turn cap to prevent unrealistic high turns
- A small, randomized chance of failure even on high levels (for realism)

  | Difficulty     | Rolls / Turn | Hold Threshold | Max Cap | Risk Style  | Behavior                        |
| -------------- | ------------ | -------------- | ------- | ----------- | ------------------------------- |
| **Noob**       | 2            | 8              | 12      | 💤 Safe     | Plays short turns, rarely busts |
| **Casual**     | 4            | 12             | 18      | 😌 Mild     | Slightly riskier, holds earlier |
| **Challenger** | 6            | 16             | 22      | ⚔️ Balanced | Even risk-reward                |
| **Veteran**    | 8            | 20             | 26      | 🎯 Moderate | Experienced player level        |
| **Elite**      | 10           | 22             | 28      | 🔥 High     | Pushes limits, still cautious   |
| **Legendary**  | 12           | 24             | 32      | 💀 Extreme  | Aggressive, near-perfect play   |




## 🧩 UML Documentation

This project includes automatically generated UML diagrams to visualize the structure of the codebase.  
The diagrams are created using **Pyreverse** (part of `pylint`) with **Graphviz** to produce graphical outputs.

### 📘 Generating UML Diagrams

To generate UML diagrams, run the following command from the project root:

```bash
make uml
```

## 📚 Code Documentation (HTML)

This project supports **automatically generated HTML documentation** based on the Python docstrings and module structure.  
The documentation is created using **Sphinx**, a popular documentation generator for Python projects.

### 🧠 Generating Documentation

You can regenerate the documentation at any time by running:

```bash
make doc
 ```

