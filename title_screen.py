import pygame
from spritesheet import Spritesheet

class TitleScreen(pygame.sprite.Sprite):
    def __init__(self):
        title_sheet = Spritesheet('spritesheet.png')
        self.ShowScreen = False
        self.current_frame = title_sheet.parse_sprite('Title1.png')
        self.last_updated = 0
        self.title_frames = []
        self.current_image = self.current_frame
        self.time = 0.2

    def update(self):
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.title_frames)
    
    def load_frames(self):
        title_sheet = Spritesheet('spritesheet.png')
        self.title_frames = [title_sheet.parse_sprite('Title1.png'),
                             title_sheet.parse_sprite('Title2.png')]
        self.current_image = self.title_frames[0]
