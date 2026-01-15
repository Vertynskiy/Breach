"""
Texture Generator for Breach game
Procedurally generates all UI textures using Pygame
No external texture files needed!
"""

import pygame
from typing import Dict, Tuple

Color = Tuple[int, int, int]

class TextureGenerator:
    """Generates procedural textures for the game"""

    COLORS = {
        'bg_dark': (15, 15, 15),
        'bg_panel': (26, 26, 26),
        'border_normal': (68, 68, 68),
        'border_light': (100, 100, 100),
        'text_primary': (255, 255, 255),
        'accent_green': (50, 220, 50),
        'accent_red': (220, 50, 50),
        'accent_yellow': (255, 220, 50),
        'accent_blue': (50, 100, 220),
        'accent_cyan': (50, 200, 200),
    }

    def __init__(self):
        self.cache: Dict[str, pygame.Surface] = {}

    @staticmethod
    def _draw_neon_border(surface: pygame.Surface, rect: pygame.Rect,
                         color: Color, width: int = 2) -> None:
        """Draw neon-style border"""
        pygame.draw.rect(surface, color, rect, width)
        glow_color = tuple(min(c + 50, 255) for c in color)
        glow_rect = rect.inflate(4, 4)
        pygame.draw.rect(surface, glow_color, glow_rect, 1)

    @staticmethod
    def _draw_gradient(surface: pygame.Surface, rect: pygame.Rect,
                      color_top: Color, color_bottom: Color) -> None:
        """Draw vertical gradient"""
        height = rect.height
        for y in range(height):
            ratio = y / max(1, height)
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(surface, (r, g, b),
                           (rect.x, rect.y + y),
                           (rect.x + rect.width, rect.y + y))

    def generate_panel(self, width: int, height: int,
                      border_color: Color = None,
                      background_color: Color = None) -> pygame.Surface:
        """Generate panel texture"""
        cache_key = f"panel_{width}_{height}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        if border_color is None:
            border_color = self.COLORS['border_normal']
        if background_color is None:
            background_color = self.COLORS['bg_panel']

        surface = pygame.Surface((width, height))
        surface.fill(background_color)

        rect = pygame.Rect(0, 0, width, height)
        self._draw_neon_border(surface, rect, border_color, width=2)

        inner_rect = pygame.Rect(2, 2, width - 4, height - 4)
        pygame.draw.rect(surface, self.COLORS['border_light'], inner_rect, 1)

        self.cache[cache_key] = surface
        return surface

    def generate_button(self, width: int, height: int,
                       state: str = 'normal') -> pygame.Surface:
        """Generate button texture"""
        cache_key = f"button_{width}_{height}_{state}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        surface = pygame.Surface((width, height))

        if state == 'normal':
            bg_color = (50, 50, 50)
            border_color = self.COLORS['border_normal']
        elif state == 'hover':
            bg_color = (85, 85, 85)
            border_color = self.COLORS['accent_green']
        elif state == 'pressed':
            bg_color = (35, 35, 35)
            border_color = self.COLORS['accent_green']
        else:
            bg_color = (50, 50, 50)
            border_color = self.COLORS['border_normal']

        surface.fill(bg_color)
        rect = pygame.Rect(0, 0, width, height)
        self._draw_neon_border(surface, rect, border_color, width=2)
        pygame.draw.line(surface, (100, 100, 100), (2, 2), (width - 2, 2), 1)

        self.cache[cache_key] = surface
        return surface

    def generate_status_bar(self, width: int, height: int,
                           fill_percent: float = 1.0,
                           bar_color: Color = None) -> pygame.Surface:
        """Generate resource bar"""
        if bar_color is None:
            bar_color = self.COLORS['accent_green']

        surface = pygame.Surface((width, height))
        surface.fill(self.COLORS['bg_dark'])

        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, self.COLORS['border_normal'], rect, 1)

        fill_width = max(2, int(width * max(0, min(1, fill_percent))))
        if fill_width > 2:
            fill_rect = pygame.Rect(1, 1, fill_width - 2, height - 2)
            pygame.draw.rect(surface, bar_color, fill_rect)

        return surface

    def generate_screen_background(self, width: int, height: int) -> pygame.Surface:
        """Generate background"""
        cache_key = f"bg_{width}_{height}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        surface = pygame.Surface((width, height))
        self._draw_gradient(surface, pygame.Rect(0, 0, width, height),
                           self.COLORS['bg_dark'],
                           self.COLORS['bg_panel'])

        for y in range(0, height, 2):
            pygame.draw.line(surface, (0, 0, 0), (0, y), (width, y), 1)

        self.cache[cache_key] = surface
        return surface

    def generate_title_bar(self, width: int, height: int,
                          glow_color: Color = None) -> pygame.Surface:
        """Generate title bar"""
        if glow_color is None:
            glow_color = self.COLORS['accent_cyan']

        surface = pygame.Surface((width, height))
        surface.fill(self.COLORS['bg_dark'])
        pygame.draw.line(surface, glow_color, (0, height - 3), (width, height - 3), 2)
        pygame.draw.line(surface, (100, 100, 120), (0, height - 1), (width, height - 1), 1)

        return surface

    def clear_cache(self):
        """Clear texture cache"""
        self.cache.clear()

# Global instance
_texture_gen = None

def get_texture_generator() -> TextureGenerator:
    """Get or create texture generator"""
    global _texture_gen
    if _texture_gen is None:
        _texture_gen = TextureGenerator()
    return _texture_gen
