import pygame
from .base import BaseState
from sprites import *
from config import *

class Gameplay(BaseState):
    def __init__(self):
        print("Overworld Gameplay")
        super(Gameplay,self).__init__()
        self.next_state = "BATTLE_SCREEN"
        #self.battle_state = "BATTLE_SCREEN"
        self.persist = {}
        
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Create spritesheets
        self.character_spritesheet = Spritesheet('img/Player/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.npc_one_spritesheet = Spritesheet('img/npc_one.png')
        self.mountain_floor_spritesheet = Spritesheet('img/Enviroment/Mountain Floor.png')


        # contains all sprites in game so they can be updated at once
        # LayeredUpdates() method searches for each update method in 
        # each sprite and calls it
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()

        self.createTilemap()
        self.createWildEnemy()
        self.startup(self.persist)

    # Creates tile map based on map in config file
    # Places a specific tile based on what letter it is
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "W":
                    Trees(self, j, i)
                if column == "P":
                    self.persist["PLAYER"] = Player(self, j, i, 2, 2, 5, 2)
                if column == "M":
                    Mountain(self, j, i)
                if column == "H":
                    House(self, j, i)
                if column == "C":
                    Cave(self, j, i)
                if column == "1":
                    NPC_One(self, j, i)
                if column == "E":
                    Mountain_Floor(self, j, i)


    def startup(self, persistent):
       persistent = self.persist

    # Create Monster for random encounter and store in persist variable
    def createWildEnemy(self):
        self.persist["ENEMY"] = Enemy(self, 3,3,5,1)

    #Reset Battle Screen State
    def reset(self):
        # Reset enemy monster for next random encounter
        self.persist["ENEMY"] = None
        self.createWildEnemy()

    # Update
    def update(self, dt):
        # Update all sprites
        # Call reset function to prepare for next encounter
        self.all_sprites.update()
        self.reset()
        
    def draw(self, surface):
        surface.fill(pygame.Color("green"))
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()