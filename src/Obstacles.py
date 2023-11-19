import pygame

"""
Obstacles are sprites that obstruct the Player's movement.
"""
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
class BlockedDoor(Obstacle):
    def __init__(self, x, y, size, room_pos):
        super().__init__(x, y, "lib/sprites/blockeddoor-1.png", size)
        
        self.room_pos = room_pos
        
        match self.room_pos:
            case "N":
                self.image = pygame.transform.rotate(self.image, 0)
            case "E":
                self.image = pygame.transform.rotate(self.image, 270)
            case "S":
                self.image = pygame.transform.rotate(self.image, 180)
            case "W":
                self.image = pygame.transform.rotate(self.image, 90)
                
class LockedDoor(Obstacle):
    def __init__(self, x, y, size, room_pos):
        super().__init__(x, y, "lib/sprites/lockeddoor-1.png", size)
        
        self.room_pos = room_pos
        
        match self.room_pos:
            case "N":
                self.image = pygame.transform.rotate(self.image, 0)
            case "E":
                self.image = pygame.transform.rotate(self.image, 270)
            case "S":
                self.image = pygame.transform.rotate(self.image, 180)
            case "W":
                self.image = pygame.transform.rotate(self.image, 90)
        
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
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/box-1.png", size)
           
class Tree(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/tree-1.png", size)
        
class Bush(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/bush-1.png", size)
        
class Rocks(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/rocks-1.png", size)
        