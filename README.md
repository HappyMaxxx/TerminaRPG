# TerminaRPG

> **Warning**: This is an old codebase written when I was still learning object-oriented programming (OOP). As a result, the code may be poorly structured, difficult to maintain, or not follow best practices. I hope to revisit and refactor it in the future to improve its quality and readability.

TerminaRPG is a text-based role-playing game (RPG) developed in Python. The game features a terminal interface where players control a hero navigating a map, engaging in combat with enemies, managing an inventory, and progressing through a dynamic world influenced by time and day-night cycles. The game supports multiple languages (English and Ukrainian) and includes a save/load system for persistent gameplay.

## Features

- **Dynamic Map Exploration**: Navigate a procedurally generated map with varied terrains (grass, mountains, water) and a fog-of-war system.
- **Combat System**: Engage in turn-based combat with enemies like goblins, skeletons, and orcs, each with unique stats and behaviors.
- **Time and Day-Night Cycle**: The game world evolves with a time system affecting enemy spawns and atmosphere (dawn, day, evening, night).
- **Inventory Management**: Collect and manage items with a limited inventory capacity.
- **Multilingual Support**: Switch between English and Ukrainian languages for menus and text.
- **Save/Load Functionality**: Save your progress and resume your adventure later.
- **Terminal-Based Interface**: Utilizes ASCII art, colored text, and a retro-style interface powered by `pyfiglet` and `colorama`.

## Prerequisites

To run TerminaRPG, you need the following:

- **Python 3.6+**
- Required Python packages:
  - `colorama`
  - `pyfiglet`

Install the dependencies using pip:

```bash
pip install colorama pyfiglet
```

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.6+ installed.
3. Install the required packages (see above).
4. Place the `main.py` and `texts.py` files in the same directory.
5. Run the game using:

```bash
python main.py
```

## How to Play

1. **Start the Game**: Run `main.py` to launch the main menu.
2. **Main Menu Options**:
   - `1`: Start a new game.
   - `2`: Load a saved game (if available).
   - `3`: How to play (not yet implemented).
   - `4`: Settings (change language between English and Ukrainian).
   - `5` or `0`: Exit the game.
3. **In-Game Controls**:
   - **Movement**: Use `W` (up), `S` (down), `D` (right), `A` (left) to move the hero (`H`).
   - **Map View**: Press `M` to view the full map.
   - **Inventory**: Press `I` to view the inventory.
   - **Commands**: Press `C` to enter command mode (not fully implemented).
   - **Escape**: Press `0` or `Esc` to pause or return to the menu.
   - **Combat**: When encountering an enemy, choose options like `1` (attack), `3` (heal), or `0` (pause).
4. **Objective**: Explore the map, fight enemies, collect coins, and survive. The game ends if the hero's HP reaches zero.

## File Structure

- `main.py`: The main game script containing all game logic, classes, and mechanics.
- `texts.py`: Contains text strings for menus, dialogues, and UI in multiple languages (not included in the provided code but referenced).
- `settings.pkl`: Stores game settings (e.g., language preference).
- `gamesave.pkl`: Stores saved game progress.

## Game Mechanics

- **Hero**: The player controls a hero with health points (HP), damage, and coins. The hero can move across the map and fight enemies.
- **Enemies**: Randomly spawned enemies (goblins, skeletons, orcs) with varying HP, damage, and healing abilities. Enemies drop coins upon defeat.
- **Map**: A 2D grid with symbols representing terrain (`♣` for grass, `▲` for mountains, `≈` for deep water, etc.). The hero's visibility is limited, revealing only a portion of the map.
- **Time System**: Tracks in-game time, affecting the day-night cycle and enemy spawn rates (more enemies at night).
- **Inventory**: A basic system to store up to 10 items (item functionality is not fully implemented).
- **Settings**: Toggle between English (`en`) and Ukrainian (`ua`) languages, saved persistently.

## Known Issues

- The `texts.py` file is missing, which may cause errors when rendering text. Ensure it exists with appropriate language dictionaries.
- The "How to Play" menu option (`3`) is not implemented.
- Some features, like advanced command mode and weapon-based combat, are incomplete or marked as TODO.
- The game relies on terminal input handling (`termios`, `tty`), which may not work consistently across all operating systems (e.g., Windows compatibility is limited).
- Error handling for edge cases (e.g., invalid map positions) could be improved.

## Future Improvements

- Implement the "How to Play" tutorial.
- Add more enemy types and items to the inventory system.
- Enhance the command mode with additional actions.
- Improve cross-platform compatibility (e.g., better Windows support for terminal input).
- Add more interactive elements, such as NPCs or quests.
- Fix potential bugs in enemy spawning and map rendering.

## Contributing

Contributions are welcome! To contribute:

1. Fork Stuart Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a clear description of your changes.

Please ensure your code follows the existing style and includes appropriate comments.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python, `colorama`, and `pyfiglet`.
- Inspired by classic text-based RPGs and roguelikes.

Enjoy your adventure in TerminaRPG!