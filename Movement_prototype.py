import pygame
import sys
import math

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulse Pursuit")

# Load sprite sheet
sprite_sheet = pygame.image.load("C:\\Users\\Ricky\\Pictures\\sCrkzvs.png")

# Flashlight parameters
cone_radius = 100
cone_height = 100
player_angle = 0  # Initial angle

# Define sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Define frames from the sprite sheet
        self.frames = []
        frame_width = sprite_sheet.get_width() // 4  # 4 frames in each row
        frame_height = sprite_sheet.get_height() // 4  # 4 frames in each column

        for i in range(4):  # Number of rows (directions)
            for j in range(4):  # Number of columns (frames per direction)
                frame = sprite_sheet.subsurface(pygame.Rect(j * frame_width, i * frame_height, frame_width, frame_height))
                self.frames.append(frame)

        self.direction = 0  # 0: Down, 1: Left, 2: Right, 3: Up
        self.index = 0
        self.image = self.frames[self.direction * 4 + self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        # Floating-point position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Distance traveled
        self.distance_traveled = 0.0

    def update(self, dx=0, dy=0):
        # Update only if there is movement
        if dx != 0 or dy != 0:
            # Update direction based on movement
            if dx > 0:
                self.direction = 2  # Right
            elif dx < 0:
                self.direction = 1  # Left
            if dy > 0:
                self.direction = 0  # Down
            elif dy < 0:
                self.direction = 3  # Up

            # Update floating-point position
            self.x += dx
            self.y += dy

            # Calculate distance traveled
            distance_moved = pygame.math.Vector2(dx, dy).length()
            self.distance_traveled += distance_moved

            # Update animation based on distance traveled
            animation_speed = 0.1  # Adjust the speed as needed
            frames_per_direction = 4
            frames_total = frames_per_direction * 4
            animation_index = int(self.distance_traveled * animation_speed) % frames_total
            self.index = animation_index % frames_per_direction

            # Round to integers for rendering
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)

            # Update image based on direction and animation index
            self.image = self.frames[self.direction * frames_per_direction + self.index]

# Set up sprite group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Set up clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse tracking
    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = math.sqrt(((mouse_x - player.rect.center[0]) ** 2) + ((mouse_y - player.rect.center[1]) ** 2))
    # Calculate the angle between player and mouse
    player_angle = math.atan2(mouse_y - player.rect.center[1], mouse_x - player.rect.center[0])

    # Player movement
    keys = pygame.key.get_pressed()
    player_speed = 2.5  # Adjust the speed as needed
    dx, dy = 0, 0

    if keys[pygame.K_LEFT]:
        dx = -player_speed
    elif keys[pygame.K_RIGHT]:
        dx = player_speed
    if keys[pygame.K_UP]:
        dy = -player_speed
    elif keys[pygame.K_DOWN]:
        dy = player_speed

    # Diagonal movement
    if dx != 0 and dy != 0:
        dx /= 1.41  # Adjust for diagonal movement to maintain the same speed
        dy /= 1.41

    # Update sprites
    all_sprites.update(dx, dy)

    # Calculate Flashlight
    # Calculate cone vertices based on the player's position and angle
    offset_factor = 0.75 + 0.25 * (1 - min(1, distance / 80))
    
    cone_vertices = [
        (
            player.rect.center[0],
            player.rect.center[1],
        ),
        # Update the point calculation with the adjusted factor
        (
            player.rect.center[0]
            + int(cone_radius * math.cos(player_angle - math.pi / 5))
            + offset_factor * int(distance * math.cos(player_angle)),
            player.rect.center[1]
            + int(cone_radius * math.sin(player_angle - math.pi / 5))
            + offset_factor * int(distance * math.sin(player_angle)),
        ),
        (
            player.rect.center[0]
            + int(cone_radius * math.cos(player_angle + math.pi / 5))
            + offset_factor * int(distance * math.cos(player_angle)),
            player.rect.center[1]
            + int(cone_radius * math.sin(player_angle + math.pi / 5))
            + offset_factor * int(distance * math.sin(player_angle)),
        )
    ]


    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw everything
    all_sprites.draw(screen)
    
    # Draw the black layer on top of the background
    black_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    black_layer.fill((0, 0, 0, 255))  # Adjust alpha value as needed
    VFXblack_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Draw the ellipse following the player
    ellipse_radius_x = 50  # Adjust the x-axis radius as needed
    ellipse_radius_y = 50  # Adjust the y-axis radius as needed
    player_center = player.rect.center
    ellipse_rect = pygame.Rect(
    player_center[0] - ellipse_radius_x,
    player_center[1] - ellipse_radius_y,
    2 * ellipse_radius_x,
    2 * ellipse_radius_y,
    )
    pygame.draw.ellipse(black_layer, (0, 0, 0, 210), ellipse_rect)
    
    # Draw the flashlight cone
    pygame.draw.polygon(black_layer, (90, 90, 0, 150) , cone_vertices)

    # Draw the ellipse following the flashlight
    ellipse_light = pygame.Rect(
    mouse_x-50,
    mouse_y-50,
    cone_radius,
    cone_radius,
    )
    pygame.draw.ellipse(black_layer, (90, 90, 0, 80), ellipse_light)

    pygame.transform.box_blur(black_layer, 20, repeat_edge_pixels=True, dest_surface=VFXblack_layer)

    # Blit the black layer onto the screen
    screen.blit(VFXblack_layer, (0, 0))

    pygame.display.flip()

    clock.tick(60)  # Adjust the frame rate as needed

# Quit the game
pygame.quit()
sys.exit()
