import pygame
from sprites import *
from config import *
from gameplay import *
from .base import *

class BattleScreen(BaseState):
    def __init__(self):
        super(BattleScreen,self).__init__()
        self.next_state = "GAME_OVER"
        self.previous_state = "GAMEPLAY"
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True