"""
UI Elements for Breach game
Buttons, text displays, panels with procedural textures
"""

import pygame
from typing import Callable, Optional, Tuple

try:
    from src.assets.texture_generator import get_texture_generator
except ImportError:
    from assets.texture_generator import get_texture_generator

Color = Tuple[int, int, int]

class Button:
    """Interactive button with visual states"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, callback: Optional[Callable] = None,
                 color: Color = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.pressed = False
        self.font = pygame.font.Font(None, 18)
        self.color = color or (50, 220, 50)

        gen = get_texture_generator()
        self.textures = {
            'normal': gen.generate_button(width, height, 'normal'),
            'hover': gen.generate_button(width, height, 'hover'),
            'pressed': gen.generate_button(width, height, 'pressed'),
        }

    def handle_event(self, event: pygame.event.EventType) -> bool:
        """Handle input. Returns True if clicked"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            self.pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.callback:
                self.callback()
            self.pressed = False

        return False

    def render(self, surface: pygame.Surface) -> None:
        """Render button"""
        if self.pressed:
            texture = self.textures['pressed']
        elif self.hovered:
            texture = self.textures['hover']
        else:
            texture = self.textures['normal']

        surface.blit(texture, self.rect)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class TextDisplay:
    """Simple text display"""

    def __init__(self, x: int, y: int, text: str = "", font_size: int = 18,
                 color: Color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)

    def update(self, text: str):
        """Update text"""
        self.text = text

    def render(self, surface: pygame.Surface):
        """Render text"""
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, (self.x, self.y))


class Panel:
    """Panel with border and background"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.title_font = pygame.font.Font(None, 28)

        self.texture = get_texture_generator().generate_panel(width, height)

    def render(self, surface: pygame.Surface):
        """Render panel"""
        surface.blit(self.texture, self.rect)

        if self.title:
            title_surf = self.title_font.render(self.title, True, (50, 220, 50))
            surface.blit(title_surf, (self.rect.x + 20, self.rect.y + 15))


class StatusBar:
    """Resource/status bar with label"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 label: str, color: Color = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.color = color or (50, 220, 50)
        self.current = 100
        self.maximum = 100

        self.label_font = pygame.font.Font(None, 16)
        self.value_font = pygame.font.Font(None, 14)

    def set_value(self, current: float, maximum: float = 100):
        """Update bar value"""
        self.current = current
        self.maximum = maximum

    def render(self, surface: pygame.Surface):
        """Render status bar"""
        gen = get_texture_generator()

        fill_percent = self.current / max(1, self.maximum)
        bar_texture = gen.generate_status_bar(self.width, self.height,
                                              fill_percent, self.color)

        surface.blit(bar_texture, (self.x, self.y))

        # Label
        label_surf = self.label_font.render(self.label, True, (255, 255, 255))
        surface.blit(label_surf, (self.x + 5, self.y - 20))

        # Value
        value_text = f"{self.current:.0f}/{self.maximum:.0f}"
        value_surf = self.value_font.render(value_text, True, (200, 200, 200))
        surface.blit(value_surf, (self.x + self.width - 50, self.y + self.height + 3))
