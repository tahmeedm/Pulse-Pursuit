import pygame
import sys
import threading
import time
import subprocess

# Start the heart rate monitor script as a subprocess
subprocess.Popen(["python", "heartratemonitor.py"])

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smooth Movement RPG Example")

# Load sprite sheet
sprite_sheet = pygame.image.load("sCrkzvs.png")

# Define sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Define frames from the sprite sheet
        self.frames = []
        frame_width = sprite_sheet.get_width() // 4
        frame_height = sprite_sheet.get_height() // 4

        for i in range(4):
            for j in range(4):
                frame = sprite_sheet.subsurface(pygame.Rect(j * frame_width, i * frame_height, frame_width, frame_height))
                self.frames.append(frame)

        self.direction = 0
        self.index = 0
        self.image = self.frames[self.direction * 4 + self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.distance_traveled = 0.0

    def update(self, dx=0, dy=0):
        if dx != 0 or dy != 0:
            if dx > 0:
                self.direction = 2
            elif dx < 0:
                self.direction = 1
            if dy > 0:
                self.direction = 0
            elif dy < 0:
                self.direction = 3

            self.x += dx
            self.y += dy
            distance_moved = pygame.math.Vector2(dx, dy).length()
            self.distance_traveled += distance_moved

            animation_speed = 0.1
            frames_per_direction = 4
            frames_total = frames_per_direction * 4
            animation_index = int(self.distance_traveled * animation_speed) % frames_total
            self.index = animation_index % frames_per_direction

            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.image = self.frames[self.direction * frames_per_direction + self.index]

# Set up sprite group
all_sprites = pygame.sprite.Group()
player = Player()
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

# Main game loop
running = True
font = pygame.font.SysFont(None, 36)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        dx /= 1.41
        dy /= 1.41

    all_sprites.update(dx, dy)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)

    heart_rate_text = font.render(f'Heart Rate: {heart_rate} BPM', True, (0, 0, 0))
    screen.blit(heart_rate_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
