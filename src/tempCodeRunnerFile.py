    # Draw interaction prompt
    if not interaction_open:
        prompt_surface = interactionfont.render(prompt_text, True, (255, 255, 255))
        prompt_surface.set_alpha(prompt_alpha)
        prompt_alpha2 = max(0,prompt_alpha2 - prompt_fade_speed)
        screen.blit(prompt_surface, (260, 400))
        screen.blit(lever_surface, (200, 100))
        screen.blit(leverMessage, (225,450))