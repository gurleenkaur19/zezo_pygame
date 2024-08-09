# ZEZO Game

A 2D survival game built using Pygame where the player must survive against waves of enemies.

## Description

In this game, you control a player character who must survive against waves of enemies. The player can shoot bullets to destroy enemies. The game ends when the player collides with an enemy.

## Installation

1. Clone the repository:

   ```sh
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```sh
   cd <project_directory>
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the game:
   ```sh
   python code/main.py
   ```
2. Use the mouse to aim and shoot at enemies.
3. Use the arrow keys or WASD to move around.
4. Survive as long as possible without colliding with enemies.

## Project Structure

- `main.py`: The main game script.
- `settings.py`: Contains game settings and constants.
- `player.py`: Defines the Player class.
- `sprites.py`: Contains various sprite classes used in the game.
- `groups.py`: Defines sprite groups used for collision detection and rendering.
- `data/maps`: Contains the map files.
- `audio`: Contains audio files for the game.
- `images`: Contains image assets for the game.

## Features

- `Player Movement` : Control the player using the keyboard.
- `Shooting Mechanism` : Aim with the mouse and shoot bullets to destroy enemies.
- `Enemy Waves` : Survive against increasing waves of enemies.
- `Game Over Screen` : Displays the number of enemies killed and the current level when the game ends.

## Controls

- `Movement` : Arrow keys or WASD
- `Shoot` : Mouse click

## Acknowledgements

- Pygame community for their excellent resources and tutorials.
- OpenGameArt for providing free game assets.
