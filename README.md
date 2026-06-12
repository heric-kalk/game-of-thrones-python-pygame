# 🐉 Game of Thrones — RPG in Pygame

> Project developed for the **Introduction to Programming** course — UFRPE, 1st Semester
> Developed over **3 months** by Computer Science students

---

## 📖 About the Project

**Game of Thrones RPG** is a 2D top-down adventure game inspired by the universe of the Game of Thrones series. The player controls **Jon Snow** on a mission to explore the vast world of Westeros, survive the dangers of the wilderness, negotiate with **Cersei Lannister**, and face the dreaded **Night King** to save the realm from the great winter.

The game was built from scratch using **Python** and the **Pygame** library, featuring an open world RPG style experience.

---

## 🎮 Gameplay

### Objective

1. Explore the map and collect **potions** to restore health.
2. Avoid or fight the **Wildlings** scattered throughout the map.
3. Find **Cersei Lannister** and try to persuade her through diplomacy.
4. Defeat the **Night King** and save Westeros!

### Main Mechanics

| Mechanic             | Description                                                                           |
| -------------------- | ------------------------------------------------------------------------------------- |
| 🗺️ Exploration      | Open world map measuring 20,000 × 20,000 pixels with a camera that follows the player |
| ⚔️ Turn-Based Combat | d20 combat system — attacks hit on a roll of 10 or higher                             |
| 🤝 Diplomacy         | Roll 5 dice (d20) and achieve 3 or more successes (DC 12) to convince Cersei          |
| 🧪 Potions           | Collect them to restore 5 HP each                                                     |
| 👾 Wildlings         | Deal 1 damage on contact and disappear from the map                                   |
| 🗓️ Mini Map         | Hold TAB to view the full map and the position of all elements                        |

---

## 🕹️ Controls

| Key             | Action                     |
| --------------- | -------------------------- |
| `W / A / S / D` | Move Jon Snow              |
| `SHIFT + WASD`  | Run                        |
| `TAB` (hold)    | Open the mini map          |
| `ENTER`         | Confirm / Roll dice        |
| `ESC`           | Return to menu / Exit game |
| `↑ / ↓`         | Navigate menus             |

---

## 🧩 Code Architecture

### Game States

The game is controlled by a state machine with 5 states:

```text
menu → game ↔ diplomacy → game
                        ↘ combat → gameover
              ↘ combat → gameover
     → config → menu
```

| State       | Description                                        |
| ----------- | -------------------------------------------------- |
| `menu`      | Main menu with Play, Settings, and Exit options    |
| `config`    | Volume sliders for music and sound effects         |
| `game`      | Open-world exploration                             |
| `diplomacy` | Dice-rolling mini-game with Cersei                 |
| `combat`    | Turn-based combat against Cersei or the Night King |
| `gameover`  | Victory or defeat screen with restart option       |

### Main Classes

**`Game`** — Orchestrates the entire game: initialization, event handling, updates, and rendering for each state.

**`Player`** — Handles movement (walking and running), directional animation using multiple sprites, collision with trees, and camera-offset rendering.

**`NPC`** — Generic entity used for Cersei, the Night King, wildlings, potions, and environmental characters.

**`Tree`** — Extends NPC with a smaller `collision_rect` at the base of the sprite, creating a depth effect.

---

## 🖥️ Requirements and Installation

### Prerequisites

* Python 3.8+
* Pygame 2.x

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/game-of-thrones-pygame.git
cd game-of-thrones-pygame

# Install dependencies
pip install pygame

# Run the game
python main.py
```

> ⚠️ Make sure the `assets/` folder is located in the project's root directory and contains all required images and audio files.

---

## 👨‍💻 Authors

Developed with dedication by **1st Semester Computer Science students — UFRPE**.

---

## 📄 License

This project was developed for academic purposes. All rights related to the **Game of Thrones** universe belong to HBO and George R. R. Martin. All artwork and audio assets are the property of their respective creators.
