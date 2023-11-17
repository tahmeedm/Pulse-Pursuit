import pygame

class Rooms:
    def __init__(self):
        self.current_room = 0
        self.room_Names = {
            "Basement" : 0, 
            "AbandonedHouse" : 1,
            "Forest" : 2,
            
        }
        self.room_backgrounds = [
            pygame.image.load("lib/sprites/bg1.jpg"),
            # Add more backgrounds as needed
        ]
        self.room_foregrounds = [
             pygame.image.load("lib/sprites/foreground.jpg"),
        ]
        self.current_background = self.room_backgrounds[0]
        self.foreground = self.room_foregrounds[0]
        self.foreground_size = (700, 500)

    def change_room(self, screen, playableArea, room_Name = "Basement"):
        room_Number = self.room_Names[room_Name]
        self.current_background = self.room_backgrounds[room_Number]
        self.foreground = self.room_foregrounds[room_Number]
        self.draw_room(screen, playableArea)

    def draw_room(self, screen, playableArea):
        # Draw the current room's background
        screen.blit(self.current_background, (0, 0))
        
        # Draw the foreground image on top of the background
        scaled_image = pygame.transform.scale(self.foreground, self.foreground_size)
        screen.blit(scaled_image, playableArea)
    
    
        
