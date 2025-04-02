import pygame, sys, random, time
from pygame.locals import *

pygame.init()

res = w, h = 1080, 720

FPS = 360 # FPS depends on speed of sprites
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SPEED = 5
SCORE = 0
# Constant of coin counter
COIN_COUNTER = 0
# Constant of player speed
PLAYER_SPEED = 5.5

SECOND_SCORE = 0
SECOND_COIN_COUNTER = 0
N = 3

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over.", True, BLACK)
 
background = pygame.image.load("/Users/macbook/Downloads/AnimatedStreet.png")
bg = pygame.transform.scale(background, (res))
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((res))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("kCHau")
 
# New class Coin which will inherit pygame's Sprite's class properties and methods 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Take image from /media/ folder and scale it 75x100
        self.image = pygame.transform.scale(pygame.image.load("/Users/macbook/Downloads/coin.png").convert_alpha(), (75, 100))
        # Creating HitBoxes of this image
        self.rect = self.image.get_rect()
        # Make it spawn randomly as enemy car
        self.rect.center = (random.randint(30, w-30),0) 
    # Move function
    def move(self):
        # Make it move the same initial speed as enemy car
        self.rect.move_ip(0, 5)
        # When it reaches top it will respawn...
        if (self.rect.top > h):
            self.rect.top = 0
            # ...also randomly
            self.rect.center = (random.randint(30, w-30), 0)
    # Gotcoin function
    def gotcoin(self):
        # When player collects (collides with coin's hitboxes)
        # Coin will respawn at the top
        self.rect.top = 0
        # at random position in x
        self.rect.center = (random.randint(30, w-30), 0)


# New class Coin which will inherit pygame's Sprite's class properties and methods 
class SpecialCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Take image from /media/ folder and scale it 75x100
        self.image = pygame.transform.scale(pygame.image.load("/Users/macbook/Downloads/Special_coin.png").convert_alpha(), (75, 100))
        # Creating HitBoxes of this image
        self.rect = self.image.get_rect()
        # Spawn it randomly of screen
        self.rect.center = (random.randint(30, w-30), 1000)
    # Move function
    def move(self):
        # Make it move the same initial speed as enemy car
        self.rect.move_ip(0, 5)
    # Spawn function
    def spawn(self):
        # Spawn in it at the top when function activated
        self.rect.top = 0
        # When it reaches top it will not respawn...
    # Gotcoin function
    def gotcoin(self):
        # When player collects (collides with coin's hitboxes)
        # Coin will not respawn at the top, but will return random value from 5 to 10
        return random.randint(5, 10)

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        # I was using my own sprites, because I didn't see sources of images before part3
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("/Users/macbook/Downloads/Enemy.png"), (100, 200)), 180)
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(30, w-30),0) 

      def move(self):
        global SCORE
        global SECOND_SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > h):
            SCORE+=1
            SECOND_SCORE+=1
            self.rect.top = 0
            self.rect.center = (random.randint(30, w-30), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(pygame.image.load("/Users/macbook/Downloads/Player.png"), (100, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, PLAYER_SPEED)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0, PLAYER_SPEED)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-PLAYER_SPEED, 0)
        if self.rect.right < w:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(PLAYER_SPEED, 0)  
 
         
P1 = Player()
E1 = Enemy()
# New constant C
C = Coin()
SC = SpecialCoin()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coin = pygame.sprite.Group()
coin.add(C)
scoin = pygame.sprite.Group()
scoin.add(SC)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C)
all_sprites.add(SC)

#Game Loop
while True:
    
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    scores = font_small.render("SCORE: " + str(SCORE), True, BLACK)
    txt = font_small.render("COINS: " + str(COIN_COUNTER), True, BLACK)
    fps = font_small.render("FPS: " + str(FPS), True, BLACK)
    DISPLAYSURF.blit(bg, (0, 0))
    DISPLAYSURF.blit(scores, (30,30))
    DISPLAYSURF.blit(txt, (w-150,30))
    DISPLAYSURF.blit(fps, (w-150,60))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    # If score counter reaches multiple of N
    if (SECOND_SCORE == N):
        SECOND_SCORE = 0 # then we reset second counter
        SC.spawn() # and spawn special coin

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('/Users/macbook/Downloads/tsis8_media_background.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (350,300))
          sc_plus_cns = font_small.render("Your score: "+str(SCORE)+". Your coins: "+str(COIN_COUNTER)+".", True, BLACK)
          DISPLAYSURF.blit(sc_plus_cns, (400,400))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()   

    #To be run if collision occurs between Player and Coin
    if pygame.sprite.spritecollideany(P1, coin):
        # Run function "gotcoin"
        C.gotcoin()
        # Add +1 to coin counter
        COIN_COUNTER+=1
        SECOND_COIN_COUNTER+=1
        # Player speed will change to +0.25 when user will collect coins, so he can move faster and avoid crashes faster
        PLAYER_SPEED = 0.25 + PLAYER_SPEED
        # Increase enemy's speed when coin counter every time reaches N coins
        if (SECOND_COIN_COUNTER == N):
            SECOND_COIN_COUNTER = 0
            SPEED+=0.25

    #To be run if collision occurs between Player and Special coin
    if pygame.sprite.spritecollideany(P1, scoin):
        # If coin is speical coin
        SC.rect.center = (random.randint(30, w-30), 2000) # Then we move it away 
        COIN_COUNTER+=SC.gotcoin() # And add random number of coin counter
        SECOND_COIN_COUNTER+=1
        if (SECOND_COIN_COUNTER >= N):
            SECOND_COIN_COUNTER = 0
            SPEED+=0.25
        PLAYER_SPEED = 0.25*SC.gotcoin() + PLAYER_SPEED

         
    pygame.display.update()
    FramePerSec.tick(FPS)