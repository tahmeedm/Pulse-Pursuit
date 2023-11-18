import pygame
from Touchables import *

class Room:
    def __init__(self, screen, playableArea):
        self.current_room = 0
        self.interactables = pygame.sprite.Group()
        self.touchables = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.playableArea = playableArea
        self.screen = screen
        self.create_room = {
            "Basement" : self.makeBasement, 
            "AbandonedHouse" : self.makeAbandonedHouse,
            "Forest" : self.makeForest    
        }
        self.room_backgrounds = [
            pygame.image.load("lib/sprites/basement walls-1.png"),
            pygame.image.load("lib/sprites/abandonedhousewalls-1.png")
            
            # Add more backgrounds as needed
        ]
        self.room_foregrounds = [
             pygame.image.load("lib/sprites/foreground.jpg"),
             pygame.image.load("lib/sprites/foreground2.png")
             
        ]
        self.current_background = self.room_backgrounds[0]
        self.foreground = self.room_foregrounds[0]
        self.foreground_size = (724, 519)

    def makeBasement(self):
        self.current_background = self.room_backgrounds[0]
        self.foreground = self.room_foregrounds[0]
        self.touchables.add(Spiketrap(256, 256, (50, 50)))
        self.touchables.add(Pillbottle(512, 512, (50, 50)))
    
    def makeAbandonedHouse(self):
        self.current_background = self.room_backgrounds[1]
        self.foreground = self.room_foregrounds[1]
        
    def makeForest(self):
        self.current_background = self.room_backgrounds[2]
        self.foreground = self.room_foregrounds[2]
    
    def set_room_type(self, room_name = "Basement"):
        self.create_room[room_name]()

    def draw_room(self):
        # Draw the current room's background
        self.screen.blit(self.current_background, (0, 0))
        
        # Draw the foreground image on top of the background
        scaled_image = pygame.transform.scale(self.foreground, self.foreground_size)
        self.screen.blit(scaled_image, self.playableArea)
        
        self.touchables.draw(self.screen)
        self.interactables.draw(self.screen)
        self.obstacles.draw(self.screen)
        
    
        
        
    
    
        
