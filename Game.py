###############################
#Date: 2024/04/19   File:Game.py
#Description: The main file for the programing competition
#Authors: Daniel Leftley, Joseph Paredes, Quincy Sy
#Spriter: Ava Jin Suen
###############################

x = 100
y = 100
import os 
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}' #Window open location

import pygame, random, math
from pygame.locals import *
pygame.init()
from pygame import mixer
from spritesheet import Spritesheet
from tiles import *
from Slime import Player
from title_screen import TitleScreen


#Un-Comment when background music made
#pygame.mixer.pre_init(44100,16,2,4096)
#pygame.mixer.music.load('')
#pygame.mixer.music.set_volume(0.5)
#pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()

canvas = pygame.Surface((800,600))
window = pygame.display.set_mode(((800,600)))

TARGET_FPS = 60

player = Player
spritesheet = Spritesheet('spritesheet.png')

spritesheet2 = Spritesheet('spritesheet(2).png')
map = TileMap('JustQuit_World1_TileLayer1.csv', spritesheet2 )

house = pygame.image.load('JustQuit_World1.png').convert()

Title_Screen = True
title = TitleScreen
#define Draw_text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    canvas.blit(img, (x, y))


while running:
    dt = clock.tick(60) * .001 * TARGET_FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #player.update(dt, map.tiles)
    
    #canvas.blit(player.current_image,(300 , 300))
    if Title_Screen:
        canvas.blit(title.current_image, (0,0))
    window.blit(canvas, (0,0))

    pygame.display.update()