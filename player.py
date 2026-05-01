import pygame # adjust import if pygame is in a different module
from constants import PLAYER_TURN_SPEED, PLAYER_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS # adjust import if constants are in a different module
from circleshape import CircleShape  # adjust import if CircleShape is in a different module
from shot import Shot # adjust import if Shot is in a different module

class Player(CircleShape): # adjust base class if CircleShape is in a different module
    def __init__(self, x, y): # adjust parameters if needed
        super().__init__(x, y, PLAYER_RADIUS) 
        self.rotation = 0 # initial rotation in degrees, facing upwards
        self.shoot_cooldown = 0.0 # cooldown timer for shooting, to prevent shooting too rapidly

    def triangle(self): # returns the vertices of the triangle representing the player
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # direction the player is facing
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 # perpendicular vector for the base of the triangle, scaled down for a sharper point
        a = self.position + forward * self.radius # tip of the triangle
        b = self.position - forward * self.radius - right # left base of the triangle
        c = self.position - forward * self.radius + right # right base of the triangle
        return [a, b, c] # return the vertices as a list of vectors

    def draw(self, screen): # draw the player as a triangle
        points = self.triangle()
        # pygame.draw.polygon expects a sequence of (x, y) pairs (floats or ints)
        pygame.draw.polygon(screen, "white", [(p.x, p.y) for p in points], LINE_WIDTH)

    def rotate(self, dt): # rotate the player based on input and delta time (this method is currently not used, but can be called from update if you want to separate rotation logic)
        self.rotation += PLAYER_TURN_SPEED * dt # rotate player based on turn speed and delta time
    
    def move(self, dt): # handle player movement based on input and delta time (this method is currently not used, but can be called from update if you want to separate movement logic
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    # This method creates a new Shot object at the player's current position and sets its velocity based on the player's rotation and a defined shooting speed. 
    def shoot(self):
        if self.shoot_cooldown > 0:
            return
        #start cooldown
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS # reset cooldown timer
        # create a new shot at the player's position
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        shot.velocity = velocity

    def update(self, dt): # handle player input and update position and rotation
        # decrease cooldown
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt) # decrease cooldown timer by delta time, ensuring it doesn't go below 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]: # rotate left
            self.rotate(-dt) # rotate left by subtracting from rotation angle
            
        if keys[pygame.K_d]: # rotate right
            self.rotate(dt) # rotate right by adding to rotation angle
        
        if keys[pygame.K_w]: # move forward
            self.move(dt) # move forward by adding to position
            
        if keys[pygame.K_s]: # move backward
            self.move(-dt) # move backward by subtracting from position)
        # wrap around screen edges (assuming screen width and height are defined)
        
        if keys[pygame.K_SPACE]: # shoot
            self.shoot() # call shoot method to create a new shot object and set its velocity based on player rotation and shooting speed