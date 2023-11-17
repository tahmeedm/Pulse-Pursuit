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
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, image_path, size)
        
    def use(self, remaining_time, player):
        player.player_speed -= 2
        player.slowed = True
        player.slowed_time = remaining_time
        return remaining_time - 60
        