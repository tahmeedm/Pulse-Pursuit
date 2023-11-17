import pygame
import math

def Peripheral_vision(player_center):
    # Draw the ellipse following the player
    ellipse_radius_x = 50  # Adjust the x-axis radius as needed
    ellipse_radius_y = 50  # Adjust the y-axis radius as needed
    ellipse_rect = pygame.Rect(
    player_center[0] - ellipse_radius_x,
    player_center[1] - ellipse_radius_y,
    2 * ellipse_radius_x,
    2 * ellipse_radius_y,
    )
    return ellipse_rect

def Flashlight_circle(mouse_x, mouse_y, cone_radius):
    # Draw the ellipse following the flashlight
    ellipse_light = pygame.Rect(
    mouse_x-50,
    mouse_y-50,
    cone_radius,
    cone_radius,
    )
    return ellipse_light

def Flashlight_cone(distance, cone_radius, player_angle, player_center):
     # Calculate cone vertices based on the player's position and angle
    offset_factor = 0.75 + 0.25 * (1 - min(1, distance / 80))
    
    cone_vertices = [
        (
            player_center[0],
            player_center[1],
        ),
        # Update the point calculation with the adjusted factor
        (
            player_center[0]
            + int(cone_radius * math.cos(player_angle - math.pi / 5))
            + offset_factor * int(distance * math.cos(player_angle)),
            player_center[1]
            + int(cone_radius * math.sin(player_angle - math.pi / 5))
            + offset_factor * int(distance * math.sin(player_angle)),
        ),
        (
            player_center[0]
            + int(cone_radius * math.cos(player_angle + math.pi / 5))
            + offset_factor * int(distance * math.cos(player_angle)),
            player_center[1]
            + int(cone_radius * math.sin(player_angle + math.pi / 5))
            + offset_factor * int(distance * math.sin(player_angle)),
        )
    ]
    return cone_vertices