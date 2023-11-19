import pygame
import sys

pygame.init()
spike_sound = pygame.mixer.Sound("lib/sounds/Trap_poke1.mp3")
speed_sound = pygame.mixer.Sound("lib/sounds/Pill_enchant1.mp3")
door_open_sound = pygame.mixer.Sound("lib/sounds/Door_open1.mp3")

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
        spike_sound.play()
        player.player_speed -= 2
        player.slowed = True
        player.slowed_time = remaining_time
        return remaining_time

class EndGoal(Touchable):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/goal.png", size)
        
    def use(self, remaining_time, player):
        pygame.quit()
        sys.exit()
   
class Pillbottle(Touchable):
    def __init__(self, x, y, size):
        super().__init__(x, y, "lib/sprites/pillbottle-1.png", size)
        
    def use(self, remaining_time, player):
        speed_sound.play()
        player.player_speed += 2
        player.hastened = True
        player.hastened_time = remaining_time
        return remaining_time

class ClosedDoor(Touchable):
    def __init__(self, x, y, size, game_map_pos, room_pos):
        super().__init__(x, y, "lib/sprites/interactabledoor-1.png", size)
        self.game_map_pos = game_map_pos
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
        
    def use(self, room, game_map, player):
        from Room import Room
        
        # Position of room in game map
        x = self.game_map_pos[0]
        y = self.game_map_pos[1]
        
        player.enter_room(self.room_pos)
        door_open_sound.play()
        
        match self.room_pos:
            case "N":
                if game_map[y-1][x] is None:
                    room = Room((x, y-1))
                    room.set_room_type()
                    room.set_door_states((0, 0, 1, 0))
                    game_map[y-1][x] = room
                    game_map[y][x].set_door_states((1, 0, 0, 0))
                else:
                    room = game_map[y-1][x]
                    room.set_door_states((0, 0, 1, 0))
                    game_map[y][x].set_door_states((1, 0, 0, 0))
            case "E":
                if game_map[y][x+1] is None:
                    room = Room((x+1, y))
                    room.set_room_type()
                    room.set_door_states((0, 0, 0, 1))
                    game_map[y][x+1] = room
                    game_map[y][x].set_door_states((0, 1, 0, 0))
                else:
                    room = game_map[y][x+1]
                    room.set_door_states((0, 0, 0, 1))
                    game_map[y][x].set_door_states((0, 1, 0, 0))
            case "S":
                if game_map[y+1][x] is None:
                    room = Room((x, y+1))
                    room.set_room_type()
                    room.set_door_states((1, 0, 0, 0))
                    game_map[y+1][x] = room
                    game_map[y][x].set_door_states((0, 0, 1, 0))
                else:
                    room = game_map[y+1][x]
                    room.set_door_states((1, 0, 0, 0))
                    game_map[y][x].set_door_states((0, 0, 1, 0))
            case "W":
                if game_map[y][x-1] is None:
                    room = Room((x-1, y))
                    room.set_room_type()
                    room.set_door_states((0, 1, 0, 0))
                    game_map[y][x-1] = room
                    game_map[y][x].set_door_states((0, 0, 0, 1))
                else:
                    room = game_map[y][x-1]
                    room.set_door_states((0, 1, 0, 0))
                    game_map[y][x].set_door_states((0, 0, 0, 1))
                    
        return room
        
class OpenedDoor(Touchable):
    def __init__(self, x, y, size, game_map_pos, room_pos):
        super().__init__(x, y, "lib/sprites/opendoor-1.png", size)
        self.game_map_pos = game_map_pos
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
    
    def use(self, game_map, player):
        # Position of room in game map
        x = self.game_map_pos[0]
        y = self.game_map_pos[1]
        
        player.enter_room(self.room_pos)
        
        match self.room_pos:
            case "N":
                y -= 1
            case "E":
                x += 1
            case "S":
                y += 1
            case "W":
                x -= 1
               
        return game_map[y][x]
    
    
