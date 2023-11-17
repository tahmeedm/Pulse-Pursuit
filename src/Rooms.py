import pygame

class Rooms:
    def __init__(self):
        self.current_room = 0
        self.room_backgrounds = [
            pygame.image.load("lib/sprites/bg1.webp"),
            #pygame.image.load("background2.png"),
            # Add more backgrounds as needed
        ]
        self.current_background = self.room_backgrounds[self.current_room]

    def change_room(self):
        self.current_room = (self.current_room + 1) % len(self.room_backgrounds)
        self.current_background = self.room_backgrounds[self.current_room]

    def draw_room(self, screen):
        # Draw the current room's background
        screen.blit(self.current_background, (0, 0))
        # Add code to draw other elements of the room based on the background