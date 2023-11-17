import pygame
import sys
import math
from Player import Player
from Flashlight import *
import threading
import time
import subprocess

# Start the heart rate monitor script as a subprocess
subprocess.Popen(["python", "heartratemonitor.py"])

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pulse Pursuit")

# Create player instance (passing the path to the sprite sheet)
player = Player("C:\\Users\\Ricky\\Pictures\\sCrkzvs.png", initial_x=350, initial_y=250)

#Load sound
walk_fast = pygame.mixer.Sound("Walk_fast1.mp3")
sound_played_walk = bool(0)
flashlight_shake = pygame.mixer.Sound("Flashlight_shake1.mp3")

# Flashlight parameters
cone_radius = 100
cone_height = 100
player_angle = 0  # Initial angle

prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
acceleration_threshold = 150 

# Set up sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set up clock
clock = pygame.time.Clock()

# Function to continuously update the heart rate from the file
def update_heart_rate():
    global heart_rate
    while True:
        try:
            with open('./hr.txt', 'r') as file:
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
        #print(f"Mouse Accelerated: {speed}") #prints out speed when high acceleration is detected
        flashlight_shake.play()
        flashlight_shake.fadeout(500)

    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y

    # Player movement
    keys = pygame.key.get_pressed()
    player_speed = 2.5
    dx, dy = 0, 0

    if keys[pygame.K_LEFT]:
        dx = -player_speed
    elif keys[pygame.K_RIGHT]:
        dx = player_speed
    if keys[pygame.K_UP]:
        dy = -player_speed
    elif keys[pygame.K_DOWN]:
        dy = player_speed

    if dx != 0 and dy != 0:

        dx /= 1.41  # Adjust for diagonal movement to maintain the same speed
        dy /= 1.41  

    if dx != 0 or dy != 0:
        if not sound_played_walk:
            sound_played_walk = True
            walk_fast.play(loops=-1)  # Set loops to -1 for infinite looping
            print(sound_played_walk)
    else:
        if sound_played_walk:
            sound_played_walk = False
            walk_fast.fadeout(500)
            print(sound_played_walk)

        dx /= 1.41
        dy /= 1.41

    all_sprites.update(dx, dy)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw everything
    all_sprites.draw(screen)
    
    # Draw the black layer on top of the background
    black_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    black_layer.fill((0, 0, 0, 255))  # Adjust alpha value as needed
    VFXblack_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Draw the peripheral vision
    pygame.draw.ellipse(black_layer, (0, 0, 0, 210), Peripheral_vision(player.rect.center))
    # Draw the flashlight cone
    pygame.draw.polygon(black_layer, (90, 90, 0, 150) , Flashlight_cone(distance, cone_radius, player_angle, player.rect.center))
    # Draw the flashlight circle
    pygame.draw.ellipse(black_layer, (90, 90, 0, 80), Flashlight_circle(mouse_x, mouse_y, cone_radius))
    # Apply Blur effect to shadows
    pygame.transform.box_blur(black_layer, 20, repeat_edge_pixels=True, dest_surface=VFXblack_layer)

    # Blit the black layer onto the screen
    screen.blit(VFXblack_layer, (0, 0))

    # Display heart rate
    heart_rate_text = font.render(f'Heart Rate: {heart_rate} BPM', True, (0, 0, 0))
    screen.blit(heart_rate_text, (10, 10))

    # Timer countdown
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds
    remaining_time = max(timer_duration - elapsed_time, 0)
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    timer_text = timer_font.render(f'{minutes}:{seconds:02}', True, (0, 0, 0))
    screen.blit(timer_text, (10, HEIGHT - 40))  # Position at the bottom-left corner

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
