# Endless Runner

A simple 2D side-scrolling endless runner game built with Python and Pygame.

## Features
- **Endless Scrolling**: The ground and obstacles continuously move towards the player, giving the illusion of running forever.
- **Dynamic Obstacles**: Includes cactuses, rocks, tall obstacles, and fast-moving fireballs.
- **Progressive Difficulty**: The game speed gradually increases as your score goes up.
- **Score System**: Tracks your current score and high score for the session.

## Installation

### Prerequisites
Make sure you have Python 3 installed. You will also need `pygame`.

### Setup
1. Clone or download this repository.
2. Install the required dependency:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```
2. **Press SPACE** to start the game.
3. **Press SPACE** while running to jump over obstacles.
4. Try to get the highest score possible!
5. If you crash, **Press SPACE** on the Game Over screen to restart.

## Assets
Currently, the game uses programmatically generated Pygame shapes (rectangles, circles, custom drawing logic) to represent the player, environment, and obstacles. This allows the game to run perfectly as a standalone application without requiring external image or sound files.

The `assets/images` and `assets/sounds` folders are provided as placeholders so you can easily replace the shapes with real sprites and sounds later.
