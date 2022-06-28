import sys
import pygame
from config import WIN_HEIGHT, WIN_WIDTH
from states.gameplay import Gameplay
from states.splash import Splash
from states.game_over import GameOver
from states.battle_screen import BattleScreen
# from states.battle_screen import BattleScreen
from states.menu import Menu
from game import Game

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
states = {
    "GAMEPLAY": Gameplay(),
    "SPLASH": Splash(),
    "GAME_OVER": GameOver(),
    "MENU": Menu(),
    "BATTLE_SCREEN": BattleScreen(),
}

game = Game(screen, states, "SPLASH")
game.run()

pygame.quit()
sys.exit()