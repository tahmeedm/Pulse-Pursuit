import pygame
import sys

class LeverGameScreen:
    def __init__(self, width, height):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = width, height
        self.FPS = 60
        self.lever_speed = 0.1

        # Colors
        self.WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)

        # Set up the screen
        self.screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # Load images and sounds
        self.lever_img = pygame.image.load("lib/sprites/Leverrod.png")
        self.base_img = pygame.image.load("C:lib/sprites/Leverbase.png")
        self.floor_img = pygame.image.load("C:lib/sprites/Floor.png")
        self.rustylever1 = pygame.mixer.Sound("lib/sounds/rustylever1.mp3")
        self.rustylever2 = pygame.mixer.Sound("lib/sounds/rustylever2.mp3")
        self.leversound = pygame.mixer.Sound("lib/sounds/Leverclick.mp3")
        self.levercrank = pygame.mixer.Sound("lib/sounds/Levercrank.mp3")
        
        # Additional attributes
        self.cycle1_played = False
        self.cycle2_played = False
        self.leversound_played = False
        self.levercrank_played = False
       
        # Initial positions
        self.lever_x = self.WIDTH // 2 - self.lever_img.get_width() // 2
        self.lever_y = self.HEIGHT // 2 - 40

        # Game state variables
        self.lever_angle = 0
        self.lever_mash_count = 0
        self.mashing = False
        self.key_cooldown = 0
        self.max_allowed_angle = 10
        self.lever_cycles = 0
        self.fixed_in_place = False
        self.final_fixed_angle = 0

    def play_lever_sound(self, cycle):
        if cycle == 0 and not self.cycle1_played:
            self.rustylever1.play()
            self.cycle1_played = True
        elif cycle == 4 and not self.cycle2_played:
            self.rustylever2.play()
            self.cycle2_played = True
        elif cycle == 7 and not self.leversound_played:
            self.leversound.play()
            self.levercrank.fadeout(500)
            self.leversound_played = True

        if not self.levercrank_played:
            self.levercrank.play(loops=-1)
            self.levercrank_played = True

    def update(self, input_key=None):
        keys = pygame.key.get_pressed()

        if keys[input_key] and self.key_cooldown == 0 and not self.fixed_in_place:
            self.mashing = True
            self.key_cooldown = 10
        elif not keys[input_key]:
            self.mashing = False

        if self.lever_cycles == 8:
            self.fixed_in_place = True
            self.final_fixed_angle = self.lever_angle

        if self.mashing and not self.fixed_in_place:
            self.lever_angle += self.lever_speed
            self.lever_mash_count += 1

            if self.lever_mash_count > 40:
                self.lever_angle = min(self.lever_angle, self.max_allowed_angle)
                self.key_cooldown = 30
                self.lever_mash_count = 0
                self.max_allowed_angle += 10
                self.play_lever_sound(self.lever_cycles)
                self.lever_cycles += 1
        elif self.fixed_in_place:
            self.lever_angle = self.final_fixed_angle

        self.screen.fill(self.BLACK)
        # Adjust positioning and scaling for lever
        rotated_lever = pygame.transform.rotate(self.lever_img, self.lever_angle)
        lever_rect = rotated_lever.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(rotated_lever, lever_rect.topleft)

        # Adjust positioning for floor
        floor_imgscaled = pygame.transform.scale(self.floor_img, (self.WIDTH, 400))
        self.screen.blit(floor_imgscaled, (0, 100))

        # Adjust positioning for base
        self.screen.blit(self.base_img, (self.WIDTH // 2 - self.base_img.get_width() // 2, self.HEIGHT - 40))

        black_rect = pygame.Surface((self.WIDTH, 200))
        self.screen.blit(black_rect, (0, 220))
        self.screen.blit(floor_imgscaled, (0, 40))
        self.screen.blit(self.base_img, (60, 200))
        pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, 400, 400), 1)

    def get_surface(self):
        return self.screen