import pygame
import sys

def draw_text(text, font, color, x, y, screen, opacity=255):
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(opacity)  # Set the text opacity
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def run_intro(width, height, screen):
    # Initialize Pygame
    pygame.init()

    # Set up fonts
    font = pygame.font.Font(None, 36)

    # Set up clock for controlling the frame rate
    clock = pygame.time.Clock()

    intro_text1 = "Pulse Pursuit"
    intro_text2 = "How you play the game is how the game plays you"

    # Initial positions
    x, y = width // 2, height // 2

    # Animation duration in seconds
    total_duration = 12.0  # Total duration of the sequence
    background_fade_duration = 5.0
    text_fade_duration = 5.0

    # Animation loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate the elapsed time
        elapsed_time = (pygame.time.get_ticks() / 1000.0)

        # Calculate the fade color and opacity for the background
        if elapsed_time < background_fade_duration:
            fade_factor_background = elapsed_time / background_fade_duration
        else:
            fade_factor_background = 1.0

        background_color = (
            int(255 * (1 - fade_factor_background)),
            int(255 * (1 - fade_factor_background)),
            int(255 * (1 - fade_factor_background)),
        )

        # Calculate the fade opacity for the text
        if background_fade_duration <= elapsed_time < total_duration:
            fade_factor_text = max(0, (elapsed_time - background_fade_duration) / text_fade_duration)
        else:
            fade_factor_text = 0

        text_opacity = int(255 * fade_factor_text)  # Opacity increases as time progresses

        # Draw the background
        screen.fill(background_color)

        # Draw the animated text
        draw_text(intro_text1, font, (255, 255, 255), x, y - 50, screen)
        draw_text(intro_text2, font, (255, 255, 255), x, y + 50, screen, text_opacity)

        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

        # Check if the animation duration has passed
        if elapsed_time >= total_duration:
            break
