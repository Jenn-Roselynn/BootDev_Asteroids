import pygame # needed for drawing and vector math
import random # needed for random asteroid spawning
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event # needed for logging events like asteroid splits

class Asteroid(CircleShape): # Asteroid class inherits from CircleShape, which provides basic properties and methods for circular shapes
    def __init__(self, x, y, radius): # constructor for the Asteroid class
        super().__init__(x, y, radius) # call the parent class constructor

    # Static method to create a random asteroid within the screen bounds
    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            "white", 
            self.position, 
            self.radius, 
            LINE_WIDTH
        )

    # Update the asteroid's position based on its velocity and the time delta
    def update(self, dt):
        self.position += (self.velocity * dt)
        
    def split(self):
        # Kill the current asteroid
        self.kill()
        # If it's small enough, don't split it
        if self.radius <= ASTEROID_MIN_RADIUS:
            log_event("Asteroid destroyed, no splitting")
            return
        # Handle splitting logic
        log_event("asteroid_split")
        
        # Random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        
        # Create two new velocity vectors by rotating the original velocity
        new_vel1 = self.velocity.rotate(random_angle)
        new_vel2 = self.velocity.rotate(-random_angle)
        
        # New radius is current radius minus the minimum radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Spawn two smaller asteroids at the same position with the new velocities and radius
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        # Assign the new velocities to the asteroids
        asteroid1.velocity = new_vel1 * 1.2 # Slightly increase speed for smaller asteroids
        asteroid2.velocity = new_vel2 * 1.2 # Slightly increase speed for smaller asteroids