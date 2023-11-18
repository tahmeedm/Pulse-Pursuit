import pygame

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


"""
Obstacles are sprites that obstruct the Player's movement.
"""
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
        
class BlockedDoor(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/lockeddoor-1.png", size)
        
class Table(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/table-1.png", size)
        
class Bed(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/bed-1.png", size)
        
class Chair(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/chair-1.png", size)
        
class Box(Obstacle):
    def __init__(self, x, y, size, screen):
        super().__init__(x, y, "lib/sprites/box-1.png", size)

    def draw(self, screen):
        self.hitbox = (self.x, self.y, 64, 64)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
           
class Tree(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/tree-1.png", size)
        
class Bush(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/bush-1.png", size)
        
class Rocks(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/rocks-1.png", size)
        