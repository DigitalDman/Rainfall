import pygame
from pygame.rect import Rect

class InventoryView:
    def __init__(self, inventory, screen, canvas) -> None:
        self.inventory = inventory
        self.canvas = canvas
        self.screen = screen
        self.slot_size = 50
        self.margin = 10
        self.font = pygame.font.Font(None, 24)
        self.item_font = pygame.font.Font(None, 18)
        self.item_color = (255, 255, 255)
        self.slot_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.slot_rects = []

    def render(self):
        
        self.canvas.fill((0, 0, 0))

        self.screen.fill((0, 0, 0))

        self.render_slots()

        self.render_items()

        pygame.display.flip()

       
    def render_slots(self):
        num_slots = len(self.inventory.slots)
        total_width = num_slots * (self.slot_size + self.margin) - self.margin
        x_offset = (self.screen.get_width() - total_width) // 2
        y_offset = (self.screen.get_height() - self.slot_size) // 2
        
        for i in range(num_slots):
            x, y = pygame.mouse.get_pos()
            slot_rect = pygame.Rect(x_offset + i * (self.slot_size + self.margin), y_offset, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(x, y):
                pygame.draw.rect(self.screen, (255, 244, 175), slot_rect)
            else:
                pygame.draw.rect(self.screen, self.slot_color, slot_rect)
            
            self.slot_rects.append(slot_rect)


    def render_items(self):
        for i, slot in enumerate(self.inventory.slots):
            if slot.type is not None:
                # Blit item's image
                item_image = slot.type.icon
                item_image_rect = item_image.get_rect(center=self.slot_rects[i].center)
                self.screen.blit(item_image, item_image_rect.topleft)

                amount_text = self.item_font.render(str(slot.amount), True, self.item_color)
                text_rect = amount_text.get_rect(bottomright=self.slot_rects[i].bottomright)
                self.screen.blit(amount_text, text_rect)
