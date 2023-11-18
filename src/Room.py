import pygame
from Touchables import *
import random as rand
WIDTH, HEIGHT = 800, 600
PLAYWIDTH, PLAYHEIGHT = 724, 519
class Room:
    def __init__(self, screen, playableArea, world_map = None):
        self.world_map = world_map
        self.interactables = pygame.sprite.Group()
        self.touchables = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        initial_position = (len(world_map) // 2, len(world_map) // 2)
        self.room_doors = [
            ClosedDoor(WIDTH // 2, 26, (32, 32), initial_position, "N"), 
            ClosedDoor(54 + PLAYWIDTH, HEIGHT // 2, (32, 32), initial_position, "E"), 
            ClosedDoor(WIDTH // 2, 56 + PLAYHEIGHT, (32, 32), initial_position, "S"), 
            ClosedDoor(24, HEIGHT // 2, (32, 32), initial_position, "W")
            ]
        self.directional_positions = {
            "N" : (WIDTH // 2, 32),
            "E" : (50 + PLAYWIDTH, HEIGHT // 2),
            "S" : (WIDTH // 2, 50 + PLAYHEIGHT),
            "W" : (30, HEIGHT // 2)
            }
        
        for i in self.room_doors:
            self.touchables.add(i)
        
        self.playableArea = playableArea
        self.screen = screen
        
        self.create_room = {
            "Basement" : self.makeBasement, 
            "AbandonedHouse" : self.makeAbandonedHouse,
            "Forest" : self.makeForest    
        }
        self.room_backgrounds = [
            pygame.image.load("lib/sprites/basement walls-1.png"),
            pygame.image.load("lib/sprites/abandonedhousewalls-1.png"),
            pygame.image.load("lib/sprites/foreground3.png") 
        ]
        self.room_foregrounds = [
             pygame.image.load("lib/sprites/foreground.jpg"),
             pygame.image.load("lib/sprites/foreground2.png"),
             pygame.image.load("lib/sprites/foreground3.png")        
        ]
        self.current_background = self.room_backgrounds[0]
        self.foreground = self.room_foregrounds[0]
        self.foreground_size = (PLAYWIDTH, PLAYHEIGHT)

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
    
    def set_room_type(self, room_name = ""):
        room_select = rand.randint % len(self.create_room)
        
        match room_select:
            case 0:
                room_select = "Basement"
            case 1:
                room_select = "AbandonedHouse"
            case 2:
                room_select = "Forest"

        if (room_name == ""):
            room_name = room_select
        
        self.create_room[room_name]()
        
    def set_door_states(self, door_states = (0, 0, 0, 0)):
        index = door_states.index(1)
        self.room_doors[index].kill()
        
        direction = ""
        match index:
            case 0:
                direction = "N"
            case 1:
                direction = "E"
            case 2:
                direction = "S"
            case 3:
                direction = "W"
        
        direction_coords = self.directional_positions[direction]
        
        self.room_doors[index] = OpenedDoor(direction_coords[0], direction_coords[1], (32, 32), (0, 0), direction)
        self.touchables.add(self.room_doors[index])    

    def draw_room(self):
        # Draw the current room's background
        self.screen.blit(self.current_background, (0, 0))
        
        # Draw the foreground image on top of the background
        scaled_image = pygame.transform.scale(self.foreground, self.foreground_size)
        self.screen.blit(scaled_image, self.playableArea)
        
        self.touchables.draw(self.screen)
        self.interactables.draw(self.screen)
        self.obstacles.draw(self.screen)
        
    
        
        
    
    
        
