import pygame
from pygame import mixer
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
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

# Image loading, sizing, scaling and turning
image_e = pygame.image.load('missile1.png')
image_p = pygame.image.load('jet.png')
image_c = pygame.image.load('cloud.png')
image_b = pygame.image.load('red_laser.png')
image_u = pygame.image.load('present.png')


size_e = (50, 35)
size_p = (75, 75)
size_c = (140,65)
size_b = (60, 20)
size_u = (65,55)

image_e = pygame.transform.scale(image_e, size_e)
image_p = pygame.transform.scale(image_p, size_p)
image_c = pygame.transform.scale(image_c, size_c)
image_b = pygame.transform.scale(image_b, size_b)
image_u = pygame.transform.scale(image_u, size_u)

image_p = pygame.transform.rotate(image_p, 270)
image_e = pygame.transform.rotate(image_e, 180)

# bara en färg variabel
red = (155, 0, 0)


# Define a player with sprite
# the surface drawn onto the screeen is player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = image_p.convert_alpha()
        
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
        self.speed = random.randint(5,17)

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        
        self.surf = image_b.convert_alpha()
        
        self.rect = self.surf.get_rect(midleft = (player.rect.midright))
    
    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Upgrade(pygame.sprite.Sprite):   
    def __init__(self):
        super(Upgrade, self).__init__()
        x = random.randint(100, 1100)
        self.surf = image_u.convert_alpha()
        self.rect = self.surf.get_rect(center = (x,0))

    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# A function for a scoreboard
def scoreboard():
    global score
    score_board = font.render('Score: '+str(score),True , red)
    scoreRect = score_board.get_rect()
    scoreRect.topright = (SCREEN_WIDTH-50, 0) 
    screen.blit(score_board, scoreRect)


# initialize pygame
pygame.init()
pygame.font.init()
score = 0
pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption('Space Game')
mixer.init()
mixer.music.load('space.mp3')
mixer.music.set_volume = (0.7)
mixer.music.play()
skjut_ljud = pygame.mixer.Sound('skjut.wav')
träff_ljud = pygame.mixer.Sound('pang.wav')
upgrade_sound = pygame.mixer.Sound('upgrade.wav')
death_sound = pygame.mixer.Sound('death.wav')
#Create the screen, based on the size choosen up top
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for framerate
clock = pygame.time.Clock()

# Create a custum event for adding a new enemy
# The + is just for unique event purpose, the number is milli-sek
ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY, 300)

# Cloud event
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 2500)

# Upgrade drop
ADDITEMS = pygame.USEREVENT + 3
pygame.time.set_timer(ADDITEMS, 5000)

#def menu():
    # En start meny

#Instantiate player.
player = Player()

#Create the Enemy sprites group, and for all other objects
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# var for running main loop
running = True

#Main loop
while running:
 
    for event in pygame.event.get():

        # Did user press key?
        if  event.type == KEYDOWN:
             # Space for bullets
            if event.key ==K_SPACE:
                new_bullet = Bullet()
                pygame.mixer.Sound.play(skjut_ljud)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)   
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
        
        # Drop an upgrade
        elif event.type == ADDITEMS:
            new_upgrade = Upgrade()
            upgrades.add(new_upgrade)
            all_sprites.add(new_upgrade)
        



    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    # update cloud
    clouds.update()
    #Update the player sprite based on user keypresses
    player.update(pressed_keys)
    #Update the enemies sprites
    enemies.update()
    
    # update bullet
    bullets.update()
    # update upgrade
    upgrades.update()
   
 # background
    screen.blit(bg, (0, 0))
    scoreboard()
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check for collisions between player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.Sound.play(death_sound)
        pygame.time.wait(1500)
        # If so, then remove the player and end the game loop
        player.kill()
        running = False
    # Bullet destroy enemy, and itself
    elif pygame.sprite.groupcollide(bullets, enemies, True, True):
        pygame.mixer.Sound.play(träff_ljud)
        score += 1000
    # Player "takes" upgrade   
    elif pygame.sprite.spritecollideany(player, upgrades):
        pygame.mixer.Sound.play(upgrade_sound)
        score += 4700
        for i in upgrades:
            i.kill()


    pygame.display.flip()
    # Set up framerate
    clock.tick(60)
# quits
pygame.quit()
