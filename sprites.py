import pygame
from pygame.locals import *
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    # defining player
    # Takes paramters game , a x position, and a y position
    def __init__(self, game, x, y, atk, defense, max_hp, lvl):
        self.game = game
        # Adds player to the player layer
        self._layer = PLAYER_LAYER
        # Adds player sprite to the all sprites group
        self.groups = self.game.all_sprites, self.game.player
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.is_alive = True

        # Player stats
        self.atk = atk
        self.defense = defense
        self.current_hp = max_hp
        self.max_hp = max_hp
        self.lvl = lvl

        # Health Bar
        self.health_bar_length = 512
        self.health_ratio = self.max_hp / self.health_bar_length

        # Set Player Spritesheet
        self.image = self.game.character_spritesheet.get_sprite(32,0, self.width, self.height)
        # List for the players down,up, left, and right animations
        self.down_animations = [self.game.character_spritesheet.get_sprite(0,0,self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32,0,self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64,0,self.width,self.height)]
        
        self.up_animations =  [self.game.character_spritesheet.get_sprite(0,96,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,96,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(64,96,self.width,self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(0,64,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,64,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(64,64,self.width,self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(64,32,self.width,self.height)]


        # Sets hit box of image to the size of the image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def basic_health(self):
        pygame.draw.rect(self.game.screen, GREEN, (512, WIN_HEIGHT-282, self.current_hp/self.health_ratio, 25))
        pygame.draw.rect(self.game.screen, BLACK, (512, WIN_HEIGHT-282, self.health_bar_length, 24), 4)

    # Update Player
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_npcs('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_npcs('y')

        self.x_change = 0
        self.y_change = 0

        self.basic_health()

    def movement(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
             # Check for random encounter at each
            self.random_encounter()
        if pressed_keys[K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
             # Check for random encounter at each step
            self.random_encounter()
        if pressed_keys[K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
             # Check for random encounter at each step
            self.random_encounter()
        if pressed_keys[K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
             # Check for random encounter at each step
            self.random_encounter()
    
    def random_encounter(self):
        chance = random.randint(0,100)
        if chance == 8:
            self.game.done = True
            self.game.battle = True

    def collide_npcs(self, direction):
        # Collision for if you are moving in the x direction
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        # Collision for if you are moving in y direction
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_boss(self, direction):
        pass

    # Collision with any sprites on BLOCK_LAYER or walls group
    def collide_blocks(self, direction):
        # Collision for if you are moving in the x direction
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        # Collision for if you are moving in y direction
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    # Function that handles Player animations
    # Includes: 4 Way directional walking
    def animate(self):
        # Decides which animation list to use depending on the direction Player is facing
        if self.facing == "down":
            # When Player is standing still, a still sprite facing down is used
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32,0,self.width, self.height)
            else:
                # Calls a animation loop
                # Animation loop goes through the list of images made above
                # Loops through the images
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32,96,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32,64,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32,32,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def equiped_items():
        pass

    def inventory():
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, name, image, atk, defense, max_hp, lvl):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.width = TILE_SIZE * 2
        self.height = TILE_SIZE * 2

        self.name = name
        self.atk = atk
        self.defense = defense
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.lvl = lvl
        self.is_alive = True

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = self.width
        self.rect.y = self.height

        # Health Bar Values
        self.health_bar_length = 512
        self.health_ratio = self.max_hp / self.health_bar_length

    def basic_health(self):
        pygame.draw.rect(self.game.screen, GREEN, (10, 10, self.current_hp/self.health_ratio, 25))
        pygame.draw.rect(self.game.screen, BLACK, (10, 10, self.health_bar_length, 24), 4)
        

class NPC_One(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.npc_one_spritesheet.get_sprite(32,0,self.width,self.height)

        # Sets hit box of image to the size of image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collide_player(self, direction):
        # Collision for if you are moving in the x direction
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.player, False)
            if hits:
                print("Testing")
                self.dialogue("Testing NPC dialogue.", self.image, self.surface)

        # Collision for if you are moving in y direction
        if direction == "y":
            print("Testing")
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                print("Testing")
                self.dialogue("Testing NPC dialogue.", self.image)

    def dialogue(self, text,icon):
        surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT/4))
        self.font = pygame.font.Font(None, 24)
        #where text is a list containing all the individual lines of text, and icon is a surface to display next to it
        surface.blit(icon,(0,surface.get_height()-64)) #paste the 64x64 image onto the bottom left of the screen
        for line in text:     #for each line we need to display
            blackBarRectPos = (64,surface.get_height()-64)  #position of the black bar at the bottom of the screen, to the right of the icon
            blackBarRectSize = (surface.get_width()-64,64)  #size of the black bar
            pygame.draw.rect(surface,(0,0,0),pygame.Rect(blackBarRectPos,blackBarRectSize)) #draw the black bar onto the screen
            textSurf = self.font.render(line,1,(255,255,255),(0,0,0))  #render the text (replace fontObject with whatever you called the font you're using for ingame text)
            surface.blit(textSurf,(80,surface.get_height()-56))  #put it onto the screen
            talk = True #variable for the while loop
            while talk: #now we have a while loop so the game effectively pauses 
                pygame.event.pump() #keep pygame updated
                if pygame.key.get_pressed()[pygame.K_SPACE]: talk = False #if the user presses spacebar
                pygame.display.flip() #keep the window active

class Trees(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64,32,self.width, self.height)

        # Sets hit box of image to the size of the image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mountain_Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.mountain_floor_spritesheet.get_sprite(32,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mountain(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(128,32, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class House(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,192, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cave(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(224, 96, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y