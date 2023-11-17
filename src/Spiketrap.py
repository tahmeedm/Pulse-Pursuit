class Spiketrap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = spiketrap_item
        self.rect = self.image.get_rect()
        self.rect.center = (256,256)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)