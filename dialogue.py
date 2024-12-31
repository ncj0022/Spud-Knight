import pygame, sys
from config import *
from states.base import *
from pygame.locals import *

class Dialogue:
    def __init__(self):
        pass

    def dialogue(screen, display_msg, border_width, border_height):
        # Draw image to the screen in order to use it as a text box
        screen.blit(panel_img, (0,0))

        font = pygame.font.Font(None, 24)
        # render text that you want on the screen
        text = font.render(display_msg, True, BLACK)
        text_rect = text.get_rect()
        pygame.draw.rect(text, BLACK, text_rect, 1)

        # draw text to screen with border width and height
        screen.blit(text, (0+border_width, 0+border_height))