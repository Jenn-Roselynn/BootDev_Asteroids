# Screen dimensions
SCREEN_WIDTH = 1280 # adjust as needed
SCREEN_HEIGHT = 720 # This is the width and height of the game window. A higher value means a larger window, while a lower value means a smaller window.

# Player constants
PLAYER_RADIUS = 20 # This is the radius of the player's ship. A higher value means a larger ship, while a lower value means a smaller ship.
LINE_WIDTH = 2 # This is the width of the lines used to draw the player and asteroids. A higher value means thicker lines, while a lower value means thinner lines.
PLAYER_TURN_SPEED = 300 # This is the speed at which the player turns, in degrees per second. A higher value means faster turning, while a lower value means slower turning.
PLAYER_SPEED = 200 # This is the speed at which the player moves. 

# Shot constants
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3 # This is the minimum time between shots. 

# Asteroid constants
ASTEROID_MIN_RADIUS = 20 # This is the radius of the smallest asteroids. A higher value means larger asteroids, while a lower value means smaller asteroids.
ASTEROID_KINDS = 3 # This is the number of different asteroid sizes. Each size will be a multiple of the minimum radius. For example, if the minimum radius is 20 and there are 3 kinds, the sizes will be 20, 40, and 60. Adjust as needed.
ASTEROID_SPAWN_RATE_SECONDS = 0.8 # This is the average time between asteroid spawns. A lower value means more frequent spawns, while a higher value means less frequent spawns.
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS # Describes the largest asteroid, which is the smallest multiplied by the number of kinds. Adjust as needed.
