import pygame

class InteractableItem(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
