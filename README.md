# Asteroids

A classic Asteroids arcade game built with Python and Pygame, developed as a guided project on [Boot.dev](https://www.boot.dev).

## Gameplay

- Pilot a spaceship and survive waves of incoming asteroids
- Shoot asteroids to destroy them — larger ones split into smaller, faster ones
- Avoid collisions or it's game over

## Features

- Player ship with rotation and thrust movement
- Shooting mechanic with cooldown
- Asteroid splitting: large → medium → small → destroyed
- Event logging for game state tracking

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

# **With uv (recommended):**

```bash
git clone https://github.com/Jenn-Roselynn/BootDev_Asteroids.git
cd BootDev_Asteroids
uv sync
uv run main.py

## With pip:
git clone https://github.com/Jenn-Roselynn/BootDev_Asteroids.git
cd BootDev_Asteroids
pip install pygame
python main.py

# CONTROLS
Key	Action
W	Thrust forward
A	Rotate left
D	Rotate right
Space	Shoot


Project Structure
File	Purpose
main.py	Game loop
player.py	Player ship logic
asteroid.py	Asteroid behavior and splitting
asteroidfield.py	Asteroid spawning
circleshape.py	Base class for circular game objects
shot.py	Projectile logic
constants.py	Game configuration values
logger.py	Event and state logging


Credits
Built following the Boot.dev Back-end Developer Path.


Just copy that into your `README.md`, adjust the controls if anything differs from your implementation, then:

```bash
git add README.md
git commit -m "Add project README"
git push origin main