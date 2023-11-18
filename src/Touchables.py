import pygame

"""
Items that are instantly interacted with when the Player touches it.
"""
class Touchable(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
    
    def use(self, player):
        """
        Item functionality.
        """
    
class Spiketrap(Touchable):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/spiketrap-1.png", size)
        
    def use(self, remaining_time, player):
        player.player_speed -= 2
        player.slowed = True
        player.slowed_time = remaining_time
        return remaining_time
        
class Pillbottle(Touchable):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/pillbottle-1.png", size)
        
    def use(self, remaining_time, player):
        player.player_speed += 2
        player.hastened = True
        player.hastened_time = remaining_time
        return remaining_time

class Door(Touchable):
    def __init__(self, x, y, size):
        super().__init__(x, y, "", size)
        
    def use(self, player, rooms):
        rooms.changeRoom()
