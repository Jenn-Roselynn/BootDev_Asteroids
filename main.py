import os # for environment variable manipulation
import sys # for system exit on game over
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # hide pygame support prompt for cleaner output
import pygame # import pygame for game development
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # import screen dimensions from constants module
from player import Player # import Player class
from shot import Shot # import Shot class
from asteroid import Asteroid # import Asteroid class
from asteroidfield import AsteroidField # import AsteroidField class
from logger import log_state, log_event  # Added log_event, this can be used later for logging specific game events like collisions, spawns, etc.

def main():
    # debug prints to verify imports and constants (can be removed later)
    print(f"--- Debug: pygame version: {pygame.version.ver} ---") # sanity check for pygame import
    print("Starting Asteroids...") # sanity check for main function
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}") # sanity check for constants import
    
    pygame.init()
    # set up the game window with specified dimensions (currently just a placeholder, can be expanded later with title, icon, etc.)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create game window
    
    # create clock for frame rate control and initialize timing variables for frame rate independent movement and FPS tracking
    clock = pygame.time.Clock() # create clock for frame rate control
    dt = 0.0  # delta time for frame rate independent movement
    frame_count = 0 # frames since last FPS print
    time_accumulator = 0.0 # time since last FPS print
    running = True # flag to control main loop
    
    # create sprite groups for managing game objects (currently just the player, but can be expanded later)
    updatable = pygame.sprite.Group() # group to hold all sprites that need updating (currently just the player, but can be expanded later)
    drawable = pygame.sprite.Group() # group to hold all sprites that need drawing (currently just the player, but can be expanded later)
    asteroids = pygame.sprite.Group() # group to hold all asteroid sprites, separate from updatable and drawable for potential future optimizations (currently not used, but can be expanded later)
    shots = pygame.sprite.Group() # group to hold all shot sprites, separate from updatable and drawable for potential future optimizations (currently not used, but can be expanded later)
    
    # CONTAINERS SETUP: set class-level containers for automatic sprite group management
    # add player to sprite groups for updating and drawing
    Player.containers = (updatable, drawable) # set class-level containers for player instances
    # make Shot automatically be added to these groups on creation
    Shot.containers = (shots, updatable, drawable) # set class-level containers for shot instances
    # make Asteroid automatically be added to these groups on creation
    Asteroid.containers = (asteroids, updatable, drawable)
    # set AsteroidField containers to only updatable and instantiate it
    AsteroidField.containers = (updatable,)
    
    # instantiate player in center of screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    # instantiate asteroid field (currently just a placeholder, can be expanded later with actual asteroid spawning and management)
    asteroid_field = AsteroidField()
    

    # main game loop
    while running: # loop until user quits
        log_state() # log game state for debugging (currently just a placeholder)
        for event in pygame.event.get(): # event handling
            if event.type == pygame.QUIT: # window close button clicked
                running = False # exit main loop
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # ESC key pressed
                running = False # exit main loop
        
        # update game state
        updatable.update(dt) # update all sprites in the updatable group
        
        # Collision Check
        for asteroid in asteroids: # check for collisions between player and asteroids
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit() # exit the game immediately on collision (can be expanded later with a game over screen, restart option, etc.)
        
        # COLLISION CHECK: SHOTS VS ASTEROIDS
        for asteroid in list(asteroids):
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    # print("Asteroid Shot!") # debug print for collision 
                    # TRIGGER THE SPLITTING LOGIC IN THE ASTEROID CLASS
                    asteroid.split() # split asteroid into smaller pieces (or kills if smaller than minimum size)
                    shot.kill() # remove shot from all groups
                    break # break inner loop to avoid checking other shots against this asteroid (since it's already destroyed)
        
        # render game state
        screen.fill((0, 0, 0)) # clear screen with black background (placeholder for actual rendering)
        # draw all sprites in the drawable group (currently just the player, but can be expanded later)
        for object in drawable: # draw all sprites in the drawable group
            object.draw(screen) # draw each object on screen
        
        # log_state() # log game state for debugging (currently just a placeholder)
        pygame.display.flip() # update the display with rendered content
        
        # cap frame rate and calculate delta time
        dt = clock.tick(60) / 1000.0  # cap to 60 FPS and get delta time (seconds)
        # print(f"dt: {dt:.6f}s")  # per-frame debug
        
        # update counters and print once per second
        frame_count += 1
        time_accumulator += dt # accumulate time since last FPS print
        if time_accumulator >= 1.0: # print FPS every second
            # print(f"dt (last frame): {dt:.6f}s  avg FPS: {frame_count/time_accumulator:.2f}")
            frame_count = 0 # reset frame count for next second
            time_accumulator = 0.0 # reset counters for next second
    # cleanup 
    pygame.quit()      # quit pygame and clean up resources when main loop exits

if __name__ == "__main__": # standard Python idiom to run main function when script is executed directly
    main() # call main function to start the game
