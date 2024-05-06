import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.FACING_RIGHT = False
        self.DOWN, self.FACING_DOWN = False, False
        self.UP, self.FACING_UP = False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.midbottom = (570, 244)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        ########################
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]
        self.left_border, self.right_border = 250, 1150
        self.ground_y = 0
        self.box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 2, self.rect.h)
        self.box.center = self.rect.center
        self.passed = False
        self.speed = .00000000000000000000000000000000000000000000000000000000000000000000001  #base gravity .35 (Boot gravity: .25)
        self.friction = -.12  
        self.position, self.velocity = pygame.math.Vector2(300,300), pygame.math.Vector2(0,0) #Normal pos = 665, 3000
        self.acceleration = pygame.math.Vector2(0,self.speed)


    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self):
        
        self.velocity = 0
        if self.LEFT_KEY:
            self.velocity = -2
        elif self.RIGHT_KEY:
            self.velocity = 2
        self.rect.x += self.velocity
        #Flight mechanics
        if self.DOWN:
            self.rect.y += self.velocityY
        elif self.UP:
            self.rect.y -= self.velocityY
        ##################
        if self.velocity == 0 and self.passed:
            self.passed = False
            self.box.center = self.rect.center
        if self.rect.x > 2800 - self.rect.w:
            self.rect.x = 2800 - self.rect.w
        elif self.rect.x < 250:
            self.rect.x = 250
        self.set_state()
        self.animate()
        if self.rect.left > self.box.left and self.rect.right < self.box.right :
            pass
        else:
            self.passed = True
            if self.rect.left > self.box.left :
                self.box.left += self.velocity
            elif self.rect.right < self.box.right :
                self.box.left += self.velocity


    def set_state(self):
        self.state = ' idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'

    def animate(self): #This code does not currently do anything. adding dt & map.tiles to player.update() made this block not work
        now = pygame.time.get_ticks()
        if self.state == ' idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]



    def load_frames(self):
        my_spritesheet = Spritesheet('spritesheet.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [my_spritesheet.parse_sprite("SlimeL1.png"),
                                 my_spritesheet.parse_sprite("SlimeL1.png")]
        self.walking_frames_left = [my_spritesheet.parse_sprite("SlimeL1.png"),
                                     my_spritesheet.parse_sprite("SlimeL2.png")]
        self.walking_frames_right = [my_spritesheet.parse_sprite("SlimeR1.png"),
                                     my_spritesheet.parse_sprite("SlimeR2.png")]
        self.walking_frames_up = [my_spritesheet.parse_sprite("SlimeU1.png"),
                                     my_spritesheet.parse_sprite("SlimeU2.png")]
        self.walking_frames_down = [my_spritesheet.parse_sprite("SlimeD1.png"),
                                     my_spritesheet.parse_sprite("SlimeD2.png")]


    Map_Made = False
    if Map_Made == False:
        def draw(self, display):
            
            display.blit(self.image, (self.rect.x, self.rect.y))

        def update(self, dt, tiles):
            self.horizontal_movement(dt)
            self.checkCollisionsx(tiles)
            self.vertical_movement(dt)
            self.checkCollisionsy(tiles)

#LETS ME MOVE
        def horizontal_movement(self,dt):
            self.acceleration.x = 0
            if self.LEFT_KEY:
                self.acceleration.x -= .09
            elif self.RIGHT_KEY:
                self.acceleration.x += .09
            self.acceleration.x += self.velocity.x * self.friction
            self.velocity.x += self.acceleration.x * dt
            self.limit_velocity(4)
            self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
            self.rect.x = self.position.x

        def vertical_movement(self,dt):
            self.acceleration.y = 0
            if self.UP:
                self.acceleration.y -= .09
            elif self.DOWN:
                self.acceleration.y += .09
            self.acceleration.y += self.velocity.y * self.friction
            self.velocity.y += self.acceleration.y * dt
            self.limit_velocity(4)
            self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
            self.rect.y = self.position.y
        
        def limit_velocity(self, max_vel):
            self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
            if abs(self.velocity.x) < .01: self.velocity.x = 0

        def get_hits(self, tiles):
            hits = []
            for tile in tiles:
                if self.rect.colliderect(tile):
                    hits.append(tile)
            return hits

        def checkCollisionsx(self, tiles):
            collisions = self.get_hits(tiles)
            for tile in collisions:
                if self.velocity.x > 0:  # Hit tile moving right
                    self.position.x = tile.rect.left - self.rect.w
                    self.rect.x = self.position.x
                elif self.velocity.x < 0:  # Hit tile moving left
                    self.position.x = tile.rect.right
                    self.rect.x = self.position.x

        def checkCollisionsy(self, tiles):
            collisions = self.get_hits(tiles)
            for tile in collisions:
                if self.velocity.y > 0:  # Hit tile moving Up
                    self.position.y = tile.rect.top - self.rect.h
                    self.rect.y = self.position.y
                elif self.velocity.y < 0:  # Hit tile moving Down
                    self.position.y = tile.rect.bottom
                    self.rect.y = self.position.y