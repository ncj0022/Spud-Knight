import pygame

WIN_WIDTH = 1024
WIN_HEIGHT = 720
TILE_SIZE = 32
FPS = 60
PLAYER_SPEED = 2

# Images
panel_img = pygame.image.load('img/panel_img.png')
# List of Enemy images
enemy_img = [pygame.image.load('img/Enemies/pipo-enemy001.png'), pygame.image.load('img/Enemies/pipo-enemy002.png'), pygame.image.load('img/Enemies/pipo-enemy003.png'),
            pygame.image.load('img/Enemies/pipo-enemy004.png'), pygame.image.load('img/Enemies/pipo-enemy005.png'), pygame.image.load('img/Enemies/pipo-enemy006.png'),
            pygame.image.load('img/Enemies/pipo-enemy007.png'), pygame.image.load('img/Enemies/pipo-enemy008.png'), pygame.image.load('img/Enemies/pipo-enemy009.png'),]
# List of Boss images


# Rendering Layers
PLAYER_LAYER = 3
NPC_LAYER = 3
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

# Color codes
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

# player stats
player_atk = 1
player_def = 1
player_lvl = 1
player_exp = 0
player_max_hp = 5
player_name = "Hero"

# Enemy stats
# self, game, name, image, atk, defense, max_hp, lvl
enemy_stats = [
    ["Bat", enemy_img[0], 1, 1, 3, 1],
    ["Wolf", enemy_img[1], 2, 1, 4, 2],
    ["Cobra", enemy_img[2], 2, 2, 2, 2]
]


# Maps
tilemap = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W.............................M.....W',
    'W..HH.........................M.....W',
    'W...1.........................B.....W',
    'W.............................M.....W',
    'WWWWWWWWWWWWWWWWWWWWWWWWW.....WWWW..W',
    'WW...WWWWWWWWH..HWWW...........WWWC.W',
    'WW...WWWWWWWW....WWWWW..........WW..W',
    'WWWW..............WWWWWWW......WWWWWW',
    'WWWWWWWWWWW.........................W',
    'WW.................1..........H..H..W',
    'WWWWWW.........................P....W',
    'WWWWWW.................WWWWWWWWWWWWWW',
    'WWWWWWWWWWW............WWWWWWWWWWWWWW',
    'WW........W............WWWWWWWWWWWWWW',
    'WWWWWW....W............WWWWWWWWWWWWWW',
    'WWWWWW....W............WWWWWWWWWWWWWW',
    'WWWWWW.................WWWWWWWWWWWWWW',
    'WWWWWWW...WW...........WWWWWWWWWWWWWW',
    'WW.HWW......MMM..................WWWW',
    'W..1.......MEEEM....................W',
    'W.........MEEEEEM................WWWW',
    'W.........EEEEEEEM..WWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
]
