import sys
import pygame
from pygame.locals import *
from config import WIN_HEIGHT, WIN_WIDTH
from states.gameplay import Gameplay
from states.splash import Splash
from states.game_over import GameOver
from states.battle_screen import BattleScreen
from states.menu import Menu
from game import Game

# Initiate Pygame
pygame.init()
# Set the screen size
flags = DOUBLEBUF
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Spud Knight')
# Instatiate all of the game states
states = {
    "GAMEPLAY": Gameplay(),
    "SPLASH": Splash(),
    "GAME_OVER": GameOver(),
    "MENU": Menu(),
    "BATTLE_SCREEN": BattleScreen(),
}

#Create our game object
game = Game(screen, states, "SPLASH")
game.run()

pygame.quit()
sys.exit()