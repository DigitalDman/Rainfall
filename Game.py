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
pygame.joystick.init()
joysticks = []
import json

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

player = Player()

##### Setting the different Areas ############
spritesheet = Spritesheet('spritesheet.png')

#Transition Screen
TransitionTime = 1
Transition = False
LoadingScreen = spritesheet.parse_sprite('LoadingScreen.png')
Loading = TileMap('Loading.csv', spritesheet)
#Town 1
LeftTown1 = False
LoadTown1 = True
Town1 = TileMap('Town1_Collision.csv', spritesheet)
Town1_display = pygame.image.load('Rainfall_perm_town.png').convert()

#Conecting Area 1
LeftCon1 = False
LoadCon1 = False
Con1 = TileMap('Con1_Collsion.csv', spritesheet)
Con1_display = pygame.image.load('ConectingArea1.png').convert()

#Conecting Area 2
LeftCon2 = False
LoadCon2 = False
Con2 = TileMap('Con2_Collision.csv', spritesheet)
Con2_display = pygame.image.load('ConectingArea2.png').convert()

#Ice Dungeon
#First Room        
LeftID_1 = False
LoadID_1 = False
ID_1 = TileMap('ID._Collsion.csv', spritesheet)
ID_1_Display = pygame.image.load('ID.png').convert()

###################################

Title_Screen = True
title = TitleScreen()
#define Draw_text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    canvas.blit(img, (x, y))

###### Showing player X & Y cords, for testing only ##########
NES_Font = pygame.font.Font('nintendo-nes-font.ttf', 10)
XYTEXT = NES_Font.render('Testing', True, (255, 255, 255))
XYRect = XYTEXT.get_rect()
XYRect.center = (150, 50)

######## ATTACKS ###########
#Dash
CanDash = False
DashTime = 0.5
DashCooldown = 2
Dash = True

##### Animateing Variable #####
FrameTime = 0.2
##### Misc. Variables ####
IsKeyboard = False
KeyTimer = 1
KeyTimeCount = False
###### Attack Selection #######



########### Text Display ##########
JoystickFont = pygame.font.Font('nintendo-nes-font.ttf', 20)
JoystickText = JoystickFont.render('This game also supports Joysticks', True, (0, 0, 0))
JoystickRect = JoystickText.get_rect()
JoystickRect.center = (450, 350)

while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            print(event)

    dt = clock.tick(60) * .001 * TARGET_FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if Title_Screen:
                if event.key == pygame.K_SPACE:
                    Title_Screen = False
            else:
                if event.key == pygame.K_a: 
                    IsKeyboard = True
                    KeyTimeCount = False
                    player.LEFT_KEY, player.FACING_LEFT = True, True
                    player.DOWN, player.RIGHT_KEY, player.UP = False, False, False
                    player.FACING_RIGHT, player.FACING_UP, player.FACING_DOWN = False, False, False
                elif event.key == pygame.K_d:
                    IsKeyboard = True
                    KeyTimeCount = False
                    player.RIGHT_KEY, player.FACING_RIGHT = True, True
                    player.FACING_DOWN, player.FACING_LEFT, player.FACING_UP = False, False, False
                    player.LEFT_KEY, player.UP, player.DOWN = False, False, False
                elif event.key == pygame.K_s:
                    IsKeyboard = True
                    KeyTimeCount = False
                    player.FACING_DOWN, player.DOWN, player.FACING_LEFT, player.FACING_UP = True, True, False, False
                    player.RIGHT_KEY, player.UP, player.LEFT_KEY = False, False, False
                elif event.key == pygame.K_w:
                    IsKeyboard = True
                    KeyTimeCount = False
                    player.UP, player.FACING_UP = True, True
                    player.FACING_DOWN, player.FACING_RIGHT, player.FACING_LEFT = False, False, False
                    player.LEFT_KEY, player.DOWN, player.RIGHT_KEY = False, False, False
                elif event.key == pygame.K_q:
                    CanDash = True
                    Dash = True
                #elif event.key == pygame.K_e: 
                
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.LEFT_KEY = False
                KeyTimeCount = True
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
                KeyTimeCount = True
            elif event.key == pygame.K_s:
                player.DOWN = False
                KeyTimeCount = True
            elif event.key == pygame.K_w:
                player.UP = False
                KeyTimeCount = True

    #player dash attack
    DashCooldown -= 1/60
    if DashTime > 0 and CanDash == False:
        Dash = False
    if DashTime < 0:
        CanDash = False
        DashCooldown = 2
        DashTime = 0.5
    if Dash:
        DashTime -= 1/60
        if player.FACING_DOWN and player.DOWN == False:
            player.position.y += 2  
            player.current_image = spritesheet.parse_sprite('DashD.png')    
        elif player.FACING_DOWN and player.DOWN:
            player.position.y += 3
            player.current_image = spritesheet.parse_sprite('DashD.png')
        elif player.FACING_UP and player.UP == False:
            player.position.y -= 2
            player.current_image = spritesheet.parse_sprite('DashU.png')
        elif player.FACING_UP and player.UP:
            player.position.y -= 3 
            player.current_image = spritesheet.parse_sprite('DashU.png')
        elif player.FACING_RIGHT and player.RIGHT_KEY == False:
            player.position.x += 2
            player.current_image = spritesheet.parse_sprite('DashR.png')
        elif player.RIGHT_KEY and player.FACING_RIGHT:
            player.position.x += 3
            player.current_image = spritesheet.parse_sprite('DashR.png')
        elif player.FACING_LEFT and player.LEFT_KEY == False:
            player.position.x -= 2
            player.current_image = spritesheet.parse_sprite('DashL.png')
        elif player.FACING_LEFT and player.LEFT_KEY:
            player.position.x -= 3
            player.current_image = spritesheet.parse_sprite('DashL.png')

    ############ Animateing the Player ##############
    FrameTime -= 1/60
    if Dash == False:
        if FrameTime > 0:
            if player.DOWN:
                player.current_image = player.walking_frames_down[0]
            elif player.UP:
                player.current_image = player.walking_frames_up[0]
            elif player.RIGHT_KEY:
                player.current_image = player.walking_frames_right[0]
            elif player.LEFT_KEY:
                player.current_image = player.walking_frames_left[0]
        elif FrameTime < 0 and FrameTime > -0.2:
            if player.FACING_DOWN:
                player.current_image = player.walking_frames_down[1]
            elif player.UP:
                player.current_image = player.walking_frames_up[1]
            elif player.RIGHT_KEY:
                player.current_image = player.walking_frames_right[1]
            elif player.LEFT_KEY:
                player.current_image = player.walking_frames_left[1]
        elif FrameTime < -0.2:
            FrameTime = 0.2

    ####### Joystick/Controller ###########
    #player movement with analogue sticks
    for joystick in joysticks:
        horiz_move = joystick.get_axis(0)
        vert_move = joystick.get_axis(1)
        if IsKeyboard == False:
            if vert_move > -2 and vert_move <= -0.5:
                player.UP, player.FACING_UP = True, True
                player.FACING_DOWN, player.FACING_RIGHT, player.FACING_LEFT = False, False, False
                player.LEFT_KEY, player.DOWN, player.RIGHT_KEY = False, False, False
            elif vert_move < 2 and vert_move >= 0.5:
                player.FACING_DOWN, player.DOWN, player.FACING_LEFT, player.FACING_UP = True, True, False, False
                player.RIGHT_KEY, player.UP, player.LEFT_KEY = False, False, False
            elif horiz_move > -2 and -0.5 > horiz_move:
                player.LEFT_KEY, player.FACING_LEFT = True, True
                player.DOWN, player.RIGHT_KEY, player.UP = False, False, False
                player.FACING_RIGHT, player.FACING_UP, player.FACING_DOWN = False, False, False
            elif horiz_move < 2 and 0.5 < horiz_move:
                player.RIGHT_KEY, player.FACING_RIGHT = True, True
                player.FACING_DOWN, player.FACING_LEFT, player.FACING_UP = False, False, False
                player.LEFT_KEY, player.UP, player.DOWN = False, False, False
            elif vert_move < 2 and vert_move < 0.5 and horiz_move < 2 and horiz_move < 0.5 and IsKeyboard == False:
                player.UP = False
                player.DOWN = False
                player.LEFT_KEY = False
                player.RIGHT_KEY = False
            ######## Button Inputs
            if joystick.get_button(0):
                CanDash = True
                Dash = True  
            if joystick.get_button(0):
                Title_Screen = False

    ######## Turning IsKeyboard to False ########
    if KeyTimeCount:
        KeyTimer -= 1/60
        if KeyTimer < 0:
            IsKeyboard = False
            KeyTimer = 1
            KeyTimeCount = False

    ############## Entering new areas ##############
    # Leaving town 1
    if LoadTown1:
        if player.rect.y < 0:
            LoadTown1 = False
            Transition = True
            LeftTown1 = True
            player.position = pygame.math.Vector2(400,560)
    if TransitionTime < 0 and LeftTown1:
        LoadCon1 = True
        LeftTown1 = False
        TransitionTime = 1
    
    # Loading Screen
    if Transition:
        TransitionTime -= 1/60
    if TransitionTime < 0:
        Transition = False

    # Leaving conecting area 1
    if LoadCon1:
        if player.rect.y < 0 or player.rect.y > 600:
            LoadCon1 = False
            Transition = True
            LeftCon1 = True
            if player.rect.y < 0:
                player.position = pygame.math.Vector2(400,560)
            elif player.rect.y > 600:
                player.position = pygame.math.Vector2(384,10)

    if TransitionTime < 0 and LeftCon1 and player.rect.y > 300:
        LoadCon2 = True
        LeftCon2 = False
        TransitionTime = 1
    if TransitionTime < 0 and LeftCon1 and player.rect.y < 500:
        LoadTown1 = True
        LeftCon1 = False
        TransitionTime = 1

    # Leaving Conecting area 2
    if LoadCon2:
        if player.rect.y < 0 or player.rect.y > 600 or player.rect.x > 800:
            LoadCon2 = False
            Transition = True
            LeftCon2 = True
            if player.rect.y < 0:
                player.position = pygame.math.Vector2(400,560)
            elif player.rect.y > 600:
                player.position = pygame.math.Vector2(400,10)
            if player.rect.x > 800:
                player.position = pygame.math.Vector2(300,300)
    #if TransitionTime < 0 and LeftCon1 and player.rect.y > 0:
     #   LoadCon1 = True
      #  LeftCon2 = False
    if TransitionTime < 0 and LeftCon2 and player.rect.y < 500:
        LoadCon1 = True
        LeftCon2 = False
        TransitionTime = 1
    if TransitionTime < 0 and LeftCon2 and player.rect.x < 500:
        LoadID_1 = True
        LeftCon2 = False
        TransitionTime = 1

    ############## Title Screen ################
    title.time -= 1/60
    if title.time > 0:
        title.current_image = spritesheet.parse_sprite('Title1.png')
    elif title.time < 0 and title.time > -0.2:
        title.current_image = spritesheet.parse_sprite('Title2.png')

    elif title.time < -0.2:
        title.time = 0.2
    title.current_image = pygame.transform.scale(title.current_image, (800, 600))
    
    player.current_image = pygame.transform.scale(player.current_image, (36, 20))
    XYTEXT = NES_Font.render('X: '+ str(player.rect.x) +"   Y: " + str(player.rect.y) , True, (255, 255, 255))
    TestText = NES_Font.render(str(Transition) , True, (255, 255, 255))

    if Title_Screen:
        canvas.blit(title.current_image, (0,0))
        canvas.blit(JoystickText,(JoystickRect))
    else:
        if Transition:
            canvas.blit(LoadingScreen, (0,0))
        if LoadTown1:
            canvas.blit(Town1_display, (0,0)) #Showing the map (use placeholder.png for testing)
        if LoadCon1:
            canvas.blit(Con1_display, (0,0))
        if LoadCon2:
            canvas.blit(Con2_display, (0,0))
        if LoadID_1:
            canvas.blit(ID_1_Display, (0,0))
        if Transition == False:
            canvas.blit(player.current_image,(player.rect.x, player.rect.y))         # Showing the player on screen
        canvas.blit(XYTEXT, XYRect) #Displaying player cordinates (Testing only)
        canvas.blit(TestText, (XYRect.x + 20 , XYRect.y + 20)) #Displaying test variables on screen 

    if LoadTown1:
        player.update(dt, Town1.tiles)
    if LoadCon1:
        player.update(dt,Con1.tiles)
    if LoadCon2:
        player.update(dt,Con2.tiles)
    if Transition:
        player.update(dt,Loading.tiles)
    if LoadID_1:
        player.update(dt, ID_1.tiles)

    window.blit(canvas, (0,0))

    pygame.display.update()