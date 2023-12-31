import pygame
from Touchables import *
from Obstacles import *
from Interactables import *
from Lever import LeverGameScreen
import random as rand

WIDTH, HEIGHT = 800, 600
PLAYWIDTH, PLAYHEIGHT = 724, 519

class Room:
    def __init__(self, initial_coords = None):
        self.interactables = pygame.sprite.Group()
        self.touchables = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        
        self.initial_position = initial_coords
        self.room_doors = [
            ClosedDoor(WIDTH // 2, 26, (32, 32), self.initial_position, "N"), 
            ClosedDoor(54 + PLAYWIDTH, HEIGHT // 2, (32, 32), self.initial_position, "E"), 
            ClosedDoor(WIDTH // 2, 56 + PLAYHEIGHT, (32, 32), self.initial_position, "S"), 
            ClosedDoor(24, HEIGHT // 2, (32, 32), self.initial_position, "W")
            ]
        self.locked_doors = [None, None, None, None]
        self.directional_positions = {
            "N" : (WIDTH // 2 - 2, 32),
            "E" : (64 + PLAYWIDTH, HEIGHT // 2),
            "S" : (WIDTH // 2 + 4, 50 + PLAYHEIGHT),
            "W" : (44, HEIGHT // 2)
            }
        
        for i in self.room_doors:
            self.touchables.add(i)
        
        # Create a list to store LeverGameScreen instances for each interactable
        self.lever_games = [LeverGameScreen(400, 400) for _ in range(2)]  # Adjust the range based on the number of interactable items
        
        self.create_room = {
            "Basement" : self.makeBasement, 
            "AbandonedHouse" : self.makeAbandonedHouse,
            "Forest" : self.makeForest,  
            "EndRoom" : self.makeEndRoom
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

        # Add all touchables/obstacles/interactables
        self.touchables.add(Spiketrap(256, 256, (50, 50)))
        self.touchables.add(Spiketrap(427, 159, (50, 50)))
        self.touchables.add(Pillbottle(512, 512, (50, 50)))
        self.touchables.add(Pillbottle(70, 450, (50, 50)))
        self.obstacle_group.add(Box(128, 120, (100, 100)))
        self.obstacle_group.add(Box(420, 400, (60, 50)))
        self.obstacle_group.add(Table(500, 125, (100, 30)))
        self.obstacle_group.add(Box(360, 400, (69, 69)))
        self.obstacle_group.add(Box(340, 300, (69, 69)))
        self.obstacle_group.add(Box(490, 300, (69, 69)))
        self.obstacle_group.add(Box(480, 400, (69, 69)))
        self.obstacle_group.add(Box(90, 500, (69, 69)))
        self.obstacle_group.add(Table(200, 500, (69, 30)))
        self.obstacle_group.add(Bed(710, 50, (90, 40)))
        self.obstacle_group.add(Box(180, 310, (50, 50)))
        self.obstacle_group.add(Box(500, 250, (69, 69)))
        self.obstacle_group.add(Box(600, 400, (64, 45)))
        self.touchables.add(Spiketrap(700, 429, (50, 50)))
        self.obstacle_group.add(Chair(610, 333, (50, 50)))
        self.obstacle_group.add(Box(669, 150, (69, 69)))
        # Locked door testing
        
        # Create item instances
        item1 = InteractableItem(370, 300, "lib/sprites/lever-1.png", (43, 35), 1) # Replace "item1.png" with the actual image file
        item2 = InteractableItem(200, 100, "lib/sprites/lever-1.png", (43, 35), 1) # Replace "item2.png" with the actual image file
        self.interactables.add(item1, item2)
        
        # Associate each interactable item with a LeverGameScreen instance
        for i, item in enumerate(self.interactables):
            item.lever_game = self.lever_games[i]
        
        # Indicate the specific door that each lever controls
        item1.lever_game.door_controlled = "S"
        item2.lever_game.door_controlled = "N"
        
        # # Add the locked doors
        # self.locked_doors[0] = LockedDoor(WIDTH // 2, 26, (32, 32), "N")
        # self.obstacle_group.add(self.locked_doors[0])
        # self.room_doors[0].kill()
        
        # self.locked_doors[2] = LockedDoor(WIDTH // 2, 56 + PLAYHEIGHT, (32, 32), "S")
        # self.obstacle_group.add(self.locked_doors[2])
        # self.room_doors[2].kill()
    
    def makeAbandonedHouse(self):
        self.current_background = self.room_backgrounds[1]
        self.foreground = self.room_foregrounds[1]

        # Add all touchables/obstacles/interactables
        self.touchables.add(Spiketrap(297, 540, (50, 30)))
        self.touchables.add(Spiketrap(186, 397, (40, 20)))
        self.touchables.add(Pillbottle(433, 258, (50, 50)))
        self.obstacle_group.add(Table(226, 289, (86, 30)))
        self.obstacle_group.add(Box(420, 406, (50, 50)))
        self.obstacle_group.add(Box(331, 197, (69, 50)))
        self.obstacle_group.add(Table(599, 179, (80, 40)))
        self.obstacle_group.add(Bed(232, 70, (80, 40)))
        self.obstacle_group.add(Box(367, 254, (100, 100)))
        self.obstacle_group.add(Chair(535, 158, (50, 50)))
        self.obstacle_group.add(Chair(666, 520, (50, 50)))
        self.obstacle_group.add(Box(650, 450, (100, 100)))
        self.obstacle_group.add(Box(70, 450, (69, 69)))
        self.obstacle_group.add(Table(100, 100, (120, 40)))
        self.touchables.add(Spiketrap(610, 320, (50, 20)))
        self.touchables.add(Spiketrap(620, 100, (50, 20)))
        self.obstacle_group.add(Box(300, 350, (70, 70)))

        item3 = InteractableItem(680, 520, "lib/sprites/lever-1.png", (43, 35), 1)
        self.interactables.add(item3)

        for i, item in enumerate(self.interactables):
            item.lever_game = self.lever_games[i]

        item3.lever_game.door_controlled = "E"


    def makeForest(self):
        self.current_background = self.room_backgrounds[2]
        self.foreground = self.room_foregrounds[2]
        self.obstacle_group.add(Tree(400, 305, (60, 200)))
        self.obstacle_group.add(Bush(300, 360, (70, 30)))
        self.obstacle_group.add(Bush(666, 555, (80, 30)))
        self.obstacle_group.add(Bush(520, 333, (80, 33)))
        self.obstacle_group.add(Bush(111, 120, (60, 30)))
        self.obstacle_group.add(Tree(666, 180, (60, 180)))
        self.obstacle_group.add(Bush(600, 120, (90, 40)))
        self.touchables.add(Pillbottle(120, 555, (50, 50)))
        self.touchables.add(Spiketrap(200, 256, (50, 25)))
        self.obstacle_group.add(Tree(200, 550, (60, 150)))
        self.obstacle_group.add(Rocks(210, 290, (30, 30)))
        self.obstacle_group.add(Rocks(360, 238, (30, 30)))
        self.obstacle_group.add(Bush(669, 420, (70, 30)))
        self.obstacle_group.add(Rocks(510, 500, (30, 30)))
        self.obstacle_group.add(Rocks(330, 111, (30, 30)))
        self.touchables.add(Pillbottle(710, 50, (50, 50)))
        self.touchables.add(Spiketrap(300, 500, (40, 30)))

        item4 = InteractableItem(70, 70, "lib/sprites/lever-1.png", (43, 35), 1)
        self.interactables.add(item4)

        for i, item in enumerate(self.interactables):
            item.lever_game = self.lever_games[i]

        item4.lever_game.door_controlled = "W"

    
    def makeEndRoom(self):
        self.makeBasement
        self.touchables.empty()
        self.touchables.add(EndGoal(WIDTH // 2 - 25, HEIGHT // 2 - 25, (50, 50)))
        self.obstacle_group.add(BlockedDoor(WIDTH // 2, 26, (32, 32), "N"))
        self.obstacle_group.add(BlockedDoor(54 + PLAYWIDTH, HEIGHT // 2, (32, 32), "E"))
        self.obstacle_group.add(BlockedDoor(WIDTH // 2, 56 + PLAYHEIGHT, (32, 32), "S"))
        self.obstacle_group.add(BlockedDoor(24, HEIGHT // 2, (32, 32), "W"))
    
    def set_room_type(self, room_name = ""):
        room_select = rand.randint(0, len(self.create_room) - 2)
        
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
        
        self.room_doors[index] = OpenedDoor(direction_coords[0], direction_coords[1], (64, 32), self.initial_position, direction)
        self.touchables.add(self.room_doors[index])    

    def draw_room(self,  screen, playableArea):
        # Draw the current room's background
        screen.blit(self.current_background, (0, 0))
        
        # Draw the foreground image on top of the background
        scaled_image = pygame.transform.scale(self.foreground, self.foreground_size)
        screen.blit(scaled_image, playableArea)
        
        self.touchables.draw(screen)
        self.interactables.draw(screen)
        self.obstacle_group.draw(screen)
        
    def unlock_door(self, door_direction):
        match door_direction:
            case "N":
                self.locked_doors[0].kill()
                self.touchables.add(self.room_doors[0])
            case "E":
                self.locked_doors[1].kill()
                self.touchables.add(self.room_doors[1])
            case "S":
                self.locked_doors[2].kill()
                self.touchables.add(self.room_doors[2])
            case "W":
                self.locked_doors[3].kill()
                self.touchables.add(self.room_doors[3])
                