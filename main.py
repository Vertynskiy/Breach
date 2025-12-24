#!/usr/bin/env python3
"""
Breach - Management Horror Game
Entry point for the game with menu support
"""

import pygame
import sys
from src.core.game_state import GameState
from src.ui.screen_manager import ScreenManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    """Main game loop"""
    pygame.init()
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breach - Management Horror")
    clock = pygame.time.Clock()
    
    # Initialize game state and UI
    game_state = GameState()
    screen_manager = ScreenManager(game_state)
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Exit on ESC key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Pass event to screen manager
            screen_manager.handle_event(event)
        
        # Update game state
        delta_time = clock.get_time() / 1000.0  # Convert ms to seconds
        game_state.update(delta_time)
        
        # Update UI
        screen_manager.update()
        
        # Render
        screen.fill((0, 0, 0))  # Black background
        screen_manager.render(screen)
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
