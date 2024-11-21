import pygame, sys
from config import *
from states.base import *
from pygame.locals import *

def dialogue(screen, border_width, border_height):
    # Draw image to the screen in order to use it as a text box
    screen.blit(panel_img, (0,0))

    font = pygame.font.Font(None, 24)
    # render text that you want on the screen
    text = font.render("This is a test of the text you want to put on the scrren.", True, BLACK)
    text_rect = text.get_rect()
    pygame.draw.rect(text, None, text_rect, 1)

    # draw text to screen with border width and height
    screen.blit(text, (0+border_width, 0+border_height))

    print("Dialogue complete")

