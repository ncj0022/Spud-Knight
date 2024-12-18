import pygame
from sprites import *
from config import *
from dialogue import *
from .gameplay import Gameplay
from .base import *

class BattleScreen(BaseState):
    def __init__(self):
        super(BattleScreen,self).__init__()
        self.active_index = 0
        self.next_state = "GAMEPLAY"
        self.persist = {}
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Set battle and skill options
        self.menu_lvl = 0
        self.msg = ""
        self.battle_options = [["Attack", "Skills", "Run"], ["Fry", "Spud", "Back"]]

    def startup(self, persistent):
        self.persist = persistent

    # Handle what happens when player chooses ATTACK action
    def player_attack(self, persistent):
        print("-----Player Turn-----")
        max_damage = round((persistent["PLAYER"].atk - persistent["ENEMY"].defense/2)/2)
        min_damage = round((persistent["PLAYER"].atk - persistent["ENEMY"].defense/2)/4)
        if min_damage <= 1 or max_damage < min_damage:
            damage = 1
        else :
            damage = random.randrange(min_damage, max_damage)
        print(damage)
        if damage > 0:
            persistent["ENEMY"].current_hp = persistent["ENEMY"].current_hp - damage
            if persistent["ENEMY"].current_hp <= 0:
                self.msg = "Your attack did nothing..."
                persistent["ENEMY"].is_alive = False
                self.is_alive(persistent)
            self.msg = persistent["ENEMY"].name + " took " + str(damage)
        else:
            print("Your attack did nothing")
            print("Enemy HP: ", persistent["ENEMY"].current_hp)
    
    # Handles the enemies turn
    def enemy_attack(self, persistent):
        print("-----Enemy Turn-----")
        max_damage = round((persistent["ENEMY"].atk - persistent["PLAYER"].defense/2)/2)
        min_damage = round((persistent["ENEMY"].atk - persistent["PLAYER"].defense/2)/4)
        if min_damage <= 0 or max_damage < min_damage:
            damage = 1
        else:
            damage = random.randrange(min_damage, max_damage)
        if damage > 0:
            persistent["PLAYER"].current_hp = persistent["PLAYER"].current_hp - damage
            if persistent["PLAYER"].current_hp <= 0:
                persistent["PLAYER"].is_alive = False
                self.is_alive(persistent)
            self.msg = persistent["PLAYER"].name + " took " + str(damage)
        else:
            print("Enemy attack did nothing.")
            print("Player HP: ", persistent["PLAYER"].current_hp)

    # Checks to see if player or enemy is alive
    # Player or enemy is alive if  hp is above 0
    def is_alive(self, persistent):
        # If player alive is false, go to game over state
        if persistent["PLAYER"].is_alive == False:
            self.next_state = "GAME_OVER"
            self.done = True
        # If enemy alive is false, return to overworld state
        elif persistent["ENEMY"].is_alive == False:
            self.next_state = "GAMEPLAY"
            exp = persistent["ENEMY"].lvl + random.randrange(1, 10)
            persistent["PLAYER"].exp += exp
            print("You won! You gained " + str(exp)+ " experience.")
            self.done = True
    
    def is_lvl_up(self, persistent):
        if self.persistent["PLAYER"].exp >= self.persistent["PLAYER"].lvl ^ 3:
            self.persistent["PLAYER"].lvl += 1
            # Address gainig multiple levels eventually

    # Render text on screen
    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.battle_options[self.menu_lvl][index], True, color)

    # Set the position of text on screen
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0] + 125, self.screen_rect.center[1] + (index * 25) + 125)
        return text.get_rect(center=center)

    # Handle when event actions happen
    def handle_action(self):
        if self.menu_lvl == 0:
            if self.active_index == 0:
                # Attack action
                self.player_attack(self.persist)
                self.enemy_attack(self.persist)
            elif self.active_index == 1:
                # Skill action
                self.menu_lvl = 1
            elif self.active_index == 2:
                self.done = True
        elif self.menu_lvl == 1:
            if self.active_index == 0:
                self.done

    # Get key inputs for events
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            # Going Up
            if event.key == pygame.K_UP:
                self.active_index = 0 if self.active_index == 1 else 1
            elif event.key == pygame.K_UP:
                self.active_index = 1 if self.active_index <= 2 else 2
            elif event.key == pygame.K_UP:
                self.active_index = 2 if self.active_index <= 0 else 0
            # Going Down
            elif event.key == pygame.K_DOWN:
                self.active_index = 0 if self.active_index >= 2 else 2
            elif event.key == pygame.K_DOWN:
                self.active_index = 1 if self.active_index == 0 else 0
            elif event.key == pygame.K_DOWN:
                self.active_index = 2 if self.active_index >= 1 else 1
            elif event.key == pygame.K_RETURN:
                self.handle_action()

    # Draw to screen battle layout
    # Draw all moves done by player and enemy to screen
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        bg = pygame.image.load("img/Forest background.png")
        surface.blit(bg, (0,0))

        # Draw enemy
        img = self.persist["ENEMY"].image

        # Draw battle gui for player
        surface.blit(img, (512-240,0))
        surface.blit(panel_img,(0,WIN_HEIGHT-282))
        surface.blit(panel_img, (WIN_WIDTH-512,WIN_HEIGHT-282))

        # Draw Player and Enemy health bars
        self.persist["PLAYER"].basic_health()
        self.persist["ENEMY"].basic_health()

        # Draw player action menu
        for index, option in enumerate(self.battle_options[0]):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))

        # Draws ddialogue box to screen but with a preset text
        # Needs to be fixed to where it updates text based on actions taking place
        dialogue(self.screen, self.msg, 24, 24)