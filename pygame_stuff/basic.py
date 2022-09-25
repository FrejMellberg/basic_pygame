import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)

# Window for game
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

#Background
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg,(SCREEN_WIDTH, SCREEN_HEIGHT))
# Image scaling and turning, eget
image_e = pygame.image.load('missile1.png')
image_p = pygame.image.load('jet.png')
image_c = pygame.image.load('cloud.png')

size_e = (50, 35)
size_p = (75, 75)
size_c = (150,60)

image_e = pygame.transform.scale(image_e, size_e)
image_p = pygame.transform.scale(image_p, size_p)
image_c = pygame.transform.scale(image_c, size_c)

image_p = pygame.transform.rotate(image_p, 270)
image_e = pygame.transform.rotate(image_e, 180)
# Define a player with sprite
# the surface drawn onto the screeen is player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = image_p.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL) 
        self.rect = self.surf.get_rect()

    #Move the sprite based on user keypresses
    def update(self, pressed_keys):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        

    # Keep player on the screen

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#Making a enemy class with sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = image_e.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(3,12)# Gissar att speed är en funktion i pyG

    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = image_c.convert_alpha()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        # Random start pos
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH +20, SCREEN_WIDTH +100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-8,0)
        if self.rect.right < 0:
            self.kill()
# initialize pygame
pygame.init()

#Create the screen, based on the size choosen up top
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for framerate
clock = pygame.time.Clock()

# Create a custum event for adding a new enemy
# The + is just for unique event purpose, the 250 is milli-sek
ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY, 550)
# Cloud event
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
#Instantiate player. just a rectangle for now
player = Player()

#Create the Enemy sprites group
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# var for running main loop
running = True

#Main loop
while running:

    for event in pygame.event.get():

        # Did user press key?
        if  event.type == KEYDOWN:
            # the escape key? then stop the loop
            if event.key == K_ESCAPE:
                running = False
        #Check for quit event
        elif event.type == QUIT:
            running = False
        #add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

         # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    #Update the player sprite based on user keypresses
    player.update(pressed_keys)
    #Update the enemies sprites
    enemies.update()
    # update cloud
    clouds.update()
   
    #Fill screen with white      
    screen.fill((0, 0, 0))
 # background
    screen.blit(bg, (0, 0))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check for collisions between player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and end the game loop
        player.kill()
        running = False

    pygame.display.flip()
    # Set up framerate
    clock.tick(60)
# quits
pygame.quit()