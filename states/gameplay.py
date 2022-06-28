import pygame
from .base import BaseState
from sprites import *
from config import *

class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay,self).__init__()
        self.next_state = "GAME_OVER"
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('img/Player/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')

        # contains all sprites in game so they can be updated at once
        # LayeredUpdates() method searches for each update method in 
        # each sprite and calls it
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        #self.enemies = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "W":
                    Wall(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "M":
                    Mountain(self, j, i)
                if column == "H":
                    House(self, j, i)
                if column == "C":
                    Cave(self, j, i)


    def update(self, dt):
        self.all_sprites.update()

    def draw(self, surface):
        surface.fill(pygame.Color("green"))
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()