import pygame
WIDTH, HEIGHT = 800, 600
class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, initial_x, initial_y):
        super().__init__()

        # Load sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path)

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
        self.hitbox = pygame.Rect(80, 80, 41, 57)
    
        self.hitbox.center = (WIDTH // 2, HEIGHT // 2)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        # Set initial position
        self.rect.x = initial_x
        self.rect.y = initial_y

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
            animation_speed = 0.05  # Adjust the speed as needed
            frames_per_direction = 4
            frames_total = frames_per_direction * 4
            animation_index = int(self.distance_traveled * animation_speed) % frames_total
            self.index = animation_index % frames_per_direction

            # Round to integers for rendering
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)

            #self.hitbox.center = (self.rect.x, self.rect.y)
            
            self.hitbox.x = round(self.x + 10)
            self.hitbox.y = round(self.y + 5)
            
            # Update image based on direction and animation index
            self.image = self.frames[self.direction * frames_per_direction + self.index]

