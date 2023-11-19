from typing import Any
import pygame

class InteractableItem(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size, sheet_col):
        super().__init__()

        # Load the entire sprite sheet
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Calculate the position of the sprite in the sheet
        self.sheet_rect = pygame.Rect(sheet_col * size[0], 0, size[0], size[1])

        # Create a subsurface using the specified rectangle
        self.image = self.sprite_sheet.subsurface(self.sheet_rect)

        # Set the rect attributes for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self, new_sheet_col):
        # Update the column in the sprite sheet
        self.sheet_rect.x = new_sheet_col * self.sheet_rect.width

        # Update the image using the modified sheet_rect
        self.image = self.sprite_sheet.subsurface(self.sheet_rect)
