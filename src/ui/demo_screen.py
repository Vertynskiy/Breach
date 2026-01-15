"""
Demo screen to test UI elements and textures
Shows all UI components in action
"""

import pygame
from src.ui.ui_elements import Button, TextDisplay, Panel, StatusBar
from src.assets.texture_generator import get_texture_generator
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE


class DemoScreen:
    """Demo screen with all UI elements"""

    def __init__(self):
        self.title_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 24)

        # Background
        self.bg_texture = get_texture_generator().generate_screen_background(
            SCREEN_WIDTH, SCREEN_HEIGHT
        )

        # Title bar
        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)

        # Panels
        self.main_panel = Panel(50, 100, 400, 500, "Resources")
        self.info_panel = Panel(480, 100, 750, 500, "Info")

        # Buttons
        self.buttons =
