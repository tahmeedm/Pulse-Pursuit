import pygame
import sys
import math
from Player import *
from Flashlight import *
from Room import *
from Touchables import *
from Interactables import *
from Lever import LeverGameScreen
from Obstacles import *
import threading
import time
import subprocess
import random

WIDTH, HEIGHT = 800, 600

# Start the heart rate monitor script as a subprocess
subprocess.Popen(["python", "src/HeartrateMonitor.py"])
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_mode((WIDTH, HEIGHT))

# Create a list to store LeverGameScreen instances for each interactable
lever_games = [LeverGameScreen(400, 400) for _ in range(2)]  # Adjust the range based on the number of interactable items
pygame.display.set_caption("Pulse Pursuit")

# Create player instance (passing the path to the sprite sheet)
player = Player("lib/sprites/player.png", initial_x=400, initial_y=300)

# Load sound
walk_fast = pygame.mixer.Sound("lib/sounds/Walk_fast1.mp3")
sound_played_walk = bool(0)
flashlight_shake = pygame.mixer.Sound("lib/sounds/Flashlight_shake1.mp3")

# Flashlight parameters
cone_radius = 150
cone_height = 100
player_angle = 0  # Initial angle
maxrange = 250

prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
acceleration_threshold = 150

# Set up sprite group
player_group = pygame.sprite.Group()
player_group.add(player)

# Create item instances
item1 = InteractableItem(400, 300, "lib/sprites/386577_stardoge_8-bit-pokeball.png", (40, 40))  # Replace "item1.png" with the actual image file
item2 = InteractableItem(200, 100, "lib/sprites/386577_stardoge_8-bit-pokeball.png", (40, 40))  # Replace "item2.png" with the actual image file
interactable_items = pygame.sprite.Group(item1, item2)

# Associate each interactable item with a LeverGameScreen instance
for i, item in enumerate(interactable_items):
    item.lever_game = lever_games[i]

# Set up interaction range
interaction_range = 50
interaction_open = False

# Set up prompt
prompt_text = "Press 'F' to Inspect"
prompt_alpha = 0
prompt_alpha2 = 0
prompt_fade_speed =  7
interactionfont = pygame.font.Font(None, 36)


# Set up clock
clock = pygame.time.Clock()

rectangle_width = 722  # Adjust the width as needed
rectangle_height = 518  # Adjust the height as needed

WIDTH, HEIGHT = 800, 600

rectangle_x = (WIDTH - rectangle_width) // 2
rectangle_y = (HEIGHT - rectangle_height) // 2

playableArea = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)

# Function to continuously update the heart rate from the file
def update_heart_rate():
    global heart_rate
    while True:
        try:
            with open('lib/hr.txt', 'r') as file:
                heart_rate = file.readline().strip()
        except:
            heart_rate = 'N/A'
        time.sleep(1)

# Thread for updating heart rate
heart_rate = '0'
heart_rate_thread = threading.Thread(target=update_heart_rate)
heart_rate_thread.daemon = True
heart_rate_thread.start()

# Timer setup
start_time = pygame.time.get_ticks()
timer_font = pygame.font.SysFont(None, 36)
timer_duration = 300  # Duration in seconds (5 minutes)
remaining_time = timer_duration

world_map_dimensions = 69
world_map = [[None for _ in range(world_map_dimensions)] for _ in range(world_map_dimensions)]

current_room_position = [world_map_dimensions // 2, world_map_dimensions // 2]


room = Room(list(current_room_position))
room.set_room_type("Basement")

world_map[current_room_position[0]][current_room_position[1]] = room

hard_pity = 30
minimum_pity = 3
end_room_pity = 0

# Main game loop
running = True
font = pygame.font.SysFont(None, 36)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse tracking
    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = math.sqrt(((mouse_x - player.rect.center[0]) ** 2) + ((mouse_y - player.rect.center[1]) ** 2))
    # Calculate the angle between player and mouse
    player_angle = math.atan2(mouse_y - player.rect.center[1], mouse_x - player.rect.center[0])

    mousedelta = pygame.math.Vector2(mouse_x - prev_mouse_x, mouse_y - prev_mouse_y)
    speed = mousedelta.length()

    if speed > acceleration_threshold:
        # print(f"Mouse Accelerated: {speed}") #prints out speed when high acceleration is detected
        flashlight_shake.play()
        flashlight_shake.fadeout(500)

    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y

    # Player movement
    keys = pygame.key.get_pressed()
    
    # Check if player is slowed
    if player.slowed:
        if remaining_time < player.slowed_time - player.slow_time:
            player.slowed = not player.slowed
            player.player_speed = Player.BASE_SPEED
            
    # Check if player is hastened
    if player.hastened:
        if remaining_time < player.hastened_time - player.haste_time:
            player.hastened = not player.hastened
            player.player_speed = Player.BASE_SPEED
    
    dx, dy = 0, 0

    if keys[pygame.K_a]:
        dx = -player.player_speed
    elif keys[pygame.K_d]:
        dx = player.player_speed
    if keys[pygame.K_w]:
        dy = -player.player_speed
    elif keys[pygame.K_s]:
        dy = player.player_speed

    if dx != 0 and dy != 0:
        dx /= 1.41  # Adjust for diagonal movement to maintain the same speed
        dy /= 1.41

    # Temporary variables for the new hitbox position
    new_hitbox_x = player.hitbox.x + dx
    new_hitbox_y = player.hitbox.y + dy

    # Create a new rect for the hitbox at the new position
    new_hitbox = pygame.Rect(new_hitbox_x, new_hitbox_y, player.hitbox.width, player.hitbox.height)

    # Check if the new hitbox would collide with any obstacles
    collide = any(new_hitbox.colliderect(obstacle.rect) for obstacle in obstacle_group)

    if white_rect.contains(pygame.Rect(new_hitbox_x, new_hitbox_y, player.hitbox.width, player.hitbox.height)) and not collide:
        # If within bounds, update the player's position and hitbox
        player.update(dx, dy)
        player.hitbox.move(dx, dy)   

    if dx != 0 or dy != 0:
        if not sound_played_walk:
            sound_played_walk = True
            walk_fast.play(loops=-1)  # Set loops to -1 for infinite looping
            # print(sound_played_walk)
    else:
        if sound_played_walk:
            sound_played_walk = False
            walk_fast.fadeout(500)
            # print(sound_played_walk)

        dx /= 1.41
        dy /= 1.41

    # Check if player touches a Touchable
    touchable = pygame.sprite.spritecollideany(player, room.touchables)
    if touchable is not None:
        
        if isinstance(touchable, ClosedDoor):
            
            r = random.randint(minimum_pity, hard_pity)
                
            direction = touchable.room_pos
            match direction:
                case "N":
                    current_room_position[1] -= 1
                case "E":
                    current_room_position[0] += 1
                case "S":
                    current_room_position[1] += 1
                case "W":
                    current_room_position[0] -= 1
            
            if(world_map[current_room_position[0]][current_room_position[1]] is None):
                end_room_pity += 1
                
            if (r <= end_room_pity and world_map[current_room_position[0]][current_room_position[1]] is None):
                room = Room(current_room_position)
                room.set_room_type("EndRoom")
                player.enter_room(direction)
            else:
                room = touchable.use(room, world_map, player)
                
        elif isinstance(touchable, OpenedDoor):
            room = touchable.use(world_map, player)
            
            direction = touchable.room_pos
            match direction:
                case "N":
                    current_room_position[1] -= 1
                case "E":
                    current_room_position[0] += 1
                case "S":
                    current_room_position[1] += 1
                case "W":
                    current_room_position[0] -= 1
            
        else:
            touchable.use(remaining_time, player)
            touchable.kill()
        
    room.draw_room(screen, playableArea)
    
        # Update prompt alpha based on player's proximity to the closest item
    closest_item = min(interactable_items, key=lambda item: pygame.math.Vector2(item.rect.centerx - player.rect.centerx, item.rect.centery - player.rect.centery).length())
    closest_distance = pygame.math.Vector2(closest_item.rect.centerx - player.rect.centerx, closest_item.rect.centery - player.rect.centery).length()
    prompt_alpha = min(255, prompt_alpha + prompt_fade_speed) if closest_distance < interaction_range else max(0, prompt_alpha - prompt_fade_speed)
    
    #Check for interactions with each item
    for item in pygame.sprite.spritecollide(player, interactable_items, False):
        # Interaction logic
        if keys[pygame.K_f] and not interaction_open:
            print(f"Interacted with the item at ({item.rect.centerx}, {item.rect.centery})!")
            interaction_open = True

        if closest_distance > interaction_range:
            interaction_open = False
                
    # Draw interactable items
    interactable_items.draw(screen)

    # Draw everything
    player_group.draw(screen)
    
    # Draw the black layer on top of the background
    black_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    black_layer.fill((0, 0, 0, 255))  # Adjust alpha value as needed
    VFXblack_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Draw the peripheral vision
    pygame.draw.ellipse(black_layer, (0, 0, 0, 210), Peripheral_vision(player.rect.center))
    # Draw the flashlight cone
    pygame.draw.polygon(black_layer, (90, 90, 0, 150), Flashlight_cone(distance, cone_radius, player_angle,player.rect.center,maxrange))
    # Draw the flashlight circle
    pygame.draw.ellipse(black_layer, (90, 90, 0, 80), Flashlight_circle(distance,mouse_x, mouse_y, cone_radius,player.rect.center,maxrange))
    # Apply Blur effect to shadows
    pygame.transform.box_blur(black_layer, 20, repeat_edge_pixels=True, dest_surface=VFXblack_layer)

    # Blit the black layer onto the screen
    screen.blit(VFXblack_layer, (0, 0))

    # Display heart rate
    heart_rate_text = font.render(f'Heart Rate: {heart_rate} BPM', True, (255, 255, 255))
    screen.blit(heart_rate_text, (10, 10))

    # Timer countdown
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds
    remaining_time = max(timer_duration - elapsed_time, 0)
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    timer_text = timer_font.render(f'{minutes}:{seconds:02}', True, (255, 255, 255))
    screen.blit(timer_text, (10, HEIGHT - 40))  # Position at the bottom-left corner

    # Draw interaction prompt
    if not interaction_open:
        prompt_surface = interactionfont.render(prompt_text, True, (255, 255, 255))
        prompt_surface.set_alpha(prompt_alpha)
        prompt_alpha2 = max(0,prompt_alpha2 - prompt_fade_speed)
        screen.blit(prompt_surface, (260, 400))
        

    # Draw interaction surface
    if interaction_open:
        interaction_surface = pygame.Surface((400, 400))

        # Find the index of the closest item in the interactable_items list
        closest_index = interactable_items.sprites().index(closest_item)
        lever_games[closest_index].update(pygame.K_SPACE)

        # Use the lever_game instance to get the surface
        lever_surface = lever_games[closest_index].get_surface()
        lever_status = lever_games[closest_index].get_global_variable()

        if lever_status == False:
            leverMessage = interactionfont.render('Hold [SPACE] to pull the lever', False, (255, 255, 255))
        else:
            leverMessage = interactionfont.render('This lever seems to be pulled', False, (255, 255, 255))

        prompt_alpha2 = min(255, prompt_alpha2 + prompt_fade_speed)

        lever_surface.set_alpha(prompt_alpha2)
        leverMessage.set_alpha(prompt_alpha2)

        # Blit lever_surface onto the interaction surface
        screen.blit(lever_surface, (200, 100))
        screen.blit(leverMessage, (225,450))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()