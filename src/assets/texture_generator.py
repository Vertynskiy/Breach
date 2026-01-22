"""
Texture Generator for Breach
Loads PNG images from assets/images/ instead of generating them
"""
import pygame
from src.assets.asset_loader import get_asset_loader


class TextureGenerator:
    """Generates or loads textures for the game"""

    def __init__(self):
        self.asset_loader = get_asset_loader()
        print("🎨 TextureGenerator инициализирован (загрузка PNG)")

    def generate_screen_background(self, width: int, height: int) -> pygame.Surface:
        """
        Загрузи фон экрана
        Для MainMenu используется bg_main_menu.png
        Для других экранов нужны свои фоны
        """
        # Пока используем заглушку - позже добавим другие фоны
        surface = pygame.Surface((width, height))
        surface.fill((20, 20, 30))  # Тёмный фон по умолчанию
        return surface

    def generate_title_bar(self, width: int, height: int) -> pygame.Surface:
        """Загрузи заголовок"""
        surface = pygame.Surface((width, height))
        surface.fill((30, 30, 50))  # Заглушка
        return surface


# Глобальный генератор текстур
_texture_generator: TextureGenerator = None


def get_texture_generator() -> TextureGenerator:
    """Получи глобальный генератор текстур"""
    global _texture_generator
    if _texture_generator is None:
        _texture_generator = TextureGenerator()
    return _texture_generator
