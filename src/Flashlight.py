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

def Flashlight_circle(distance,mouse_x, mouse_y, cone_radius, player_center,maxrange):
    # Draw the ellipse following the flashlight
    if distance > maxrange:
        delta_x = mouse_x - player_center[0]
        delta_y = mouse_y - player_center[1]
        
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
        
        # Calculate the unit vector components
        unit_vector_x = delta_x / magnitude
        unit_vector_y = delta_y / magnitude
        
        # Scale the unit vector by the desired distance
        scaled_vector_x = maxrange * unit_vector_x
        scaled_vector_y = maxrange * unit_vector_y
        
        # Calculate the position of the ellipse relative to the player
        ellipse_x = player_center[0] + scaled_vector_x
        ellipse_y = player_center[1] + scaled_vector_y
        
        # Create the ellipse Rect
        ellipse_light = pygame.Rect(
            ellipse_x - cone_radius / 2,
            ellipse_y - cone_radius / 2,
            cone_radius,
            cone_radius,
        )
    else:
        ellipse_light = pygame.Rect(
        mouse_x-cone_radius/2,
        mouse_y-cone_radius/2,
        cone_radius,
        cone_radius,
        )
    return ellipse_light

def Flashlight_cone(distance, cone_radius, player_angle, player_center,maxrange):
     # Calculate cone vertices based on the player's position and angle
    if distance > maxrange:
        distance = maxrange
    calcdistance = distance-(cone_radius/1.41)
    
    cone_vertices = [
        (
            player_center[0],
            player_center[1],
        ),
        # Update the point calculation with the adjusted factor
        (
            player_center[0]
            + int(cone_radius * math.cos(player_angle - math.pi / 5))
            + 1 * int(calcdistance * math.cos(player_angle)),
            player_center[1]
            + int(cone_radius * math.sin(player_angle - math.pi / 5))
            + 1 * int(calcdistance * math.sin(player_angle)),
        ),
        (
            player_center[0]
            + int(cone_radius * math.cos(player_angle + math.pi / 5))
            + 1 * int(calcdistance * math.cos(player_angle)),
            player_center[1]
            + int(cone_radius * math.sin(player_angle + math.pi / 5))
            + 1 * int(calcdistance * math.sin(player_angle)),
        )
    ]
    return cone_vertices