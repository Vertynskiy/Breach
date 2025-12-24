#!/usr/bin/env python3
"""
Breach - Management Horror Game
Entry point for the game
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
            
            # Pass event to screen manager
            screen_manager.handle_event(event)
        
        # Update game state
        game_state.update(clock.get_time() / 1000.0)  # Convert ms to seconds
        
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
