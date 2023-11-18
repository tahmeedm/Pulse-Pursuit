import pygame
import random

"""
Items that are instantly interacted with when the Player touches it.
"""
class Touchable(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image_path, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect(center=(x, y))
    
    def use(self):
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

class ClosedDoor(Touchable):
    def __init__(self, x, y, size, game_map_pos, room_pos):
        super().__init__(x, y, "lib/sprites/interactabledoor-1.png", size)
        self.game_map_pos = game_map_pos
        self.room_pos = room_pos
        
    def use(self, game_map):
        room = Room()
        
        # Random number generator
        rand = random.randrange(3)
        match rand:
            case 0: # Basement
                room.set_room_type("Basement")
            case 1: # Abandoned House
                room.set_room_type("Abandoned House")                
            case 2: # Forest
                room.set_room_type("Forest")
        
        # Position of room in game map
        x = self.game_map_pos[0]
        y = self.game_map_pos[1]
        
        match self.room_pos:
            case "N":
                room.set_door_states((0, 0, 1, 0))
                game_map[x][y].set_door_states((1, 0, 0, 0))
                game_map[x][y-1] = room
            case "E":
                room.set_door_states((0, 0, 0, 1))
                game_map[x][y].set_door_states((0, 1, 0, 0))
                game_map[x+1][y] = room
            case "S":
                room.set_door_states((1, 0, 0, 0))
                game_map[x][y].set_door_states((0, 0, 1, 0))
                game_map[x][y+1] = room
            case "W":
                room.set_door_states((0, 1, 0, 0))
                game_map[x][y].set_door_states((0, 0, 0, 1))
                game_map[x-1][y] = room
            
        return room
                
class OpenedDoor(Touchable):
    def __init__(self, x, y, size, game_map_pos, room_pos):
        super().__init__(x, y, "lib/sprites/opendoor-1.png", size)
        self.game_map_pos = game_map_pos
        self.room_pos = room_pos
    
    def use(self, game_map):
        x = self.game_map_pos[0]
        y = self.game_map_pos[1]
        
        match self.room_pos:
            case "N":
                y -= 1
            case "E":
                x += 1
            case "S":
                y += 1
            case "W":
                x -= 1
               
        return game_map[x][y]
