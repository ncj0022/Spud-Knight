import pygame
from config import *
from sprites import *

class Dialogue:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.text_box = panel_img

    def draw_textbox(screen, box_img, box_pos):
        screen.blit(box_img, box_pos)

    # Render text on screen
    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.battle_options[self.menu_lvl][index], True, color)

    # Set the position of text on screen
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0] + 125, self.screen_rect.center[1] + (index * 25) + 125)
        return text.get_rect(center=center)

    def talk(text):
        pass