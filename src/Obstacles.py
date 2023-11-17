import pygame

"""
Obstacles are sprites that obstruct the Player's movement.
"""
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
        
class Table(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Bed(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Chair(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Box(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Tree(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Bush(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        
class Rock(Obstacle):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, "", size)
        