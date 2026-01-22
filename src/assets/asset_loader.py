"""
Asset Loader for Breach
Loads PNG images from assets/images/ directory
"""
import os
import pygame
from typing import Dict, Optional


class AssetLoader:
    """Loads and caches game assets (images)"""

    def __init__(self):
        self.assets_dir = "assets/images"
        self.cache: Dict[str, pygame.Surface] = {}
        self.missing_assets: set = set()

        # Проверь, что папка существует
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir, exist_ok=True)
            print(f"⚠️ Создана папка {self.assets_dir} - положи туда PNG файлы!")

    def load(self, filename: str) -> Optional[pygame.Surface]:
        """
        Загрузи изображение из файла

        Args:
            filename: имя файла без расширения (например, 'bg_main_menu')

        Returns:
            pygame.Surface или None если файл не найден
        """
        # Если уже в кеше - верни из кеша
        if filename in self.cache:
            return self.cache[filename]

        filepath = f"{self.assets_dir}/{filename}.png"

        # Проверь, существует ли файл
        if not os.path.exists(filepath):
            if filename not in self.missing_assets:
                print(f"❌ ОШИБКА: Не найден файл {filepath}")
                self.missing_assets.add(filename)
            return None

        try:
            # Загрузи изображение
            image = pygame.image.load(filepath)
            image = image.convert()  # Оптимизация для Pygame

            # Сохрани в кеш
            self.cache[filename] = image
            print(f"✅ Загружен: {filename}.png ({image.get_width()}x{image.get_height()})")

            return image

        except pygame.error as e:
            print(f"❌ Ошибка при загрузке {filepath}: {e}")
            return None

    def get_size(self, filename: str) -> Optional[tuple]:
        """Получи размер изображения (width, height)"""
        image = self.load(filename)
        if image:
            return image.get_size()
        return None

    def clear_cache(self):
        """Очисти кеш"""
        self.cache.clear()
        print("✅ Кеш очищен")


# Глобальный загрузчик активов (singleton)
_asset_loader: Optional[AssetLoader] = None


def get_asset_loader() -> AssetLoader:
    """Получи глобальный загрузчик активов"""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = AssetLoader()
    return _asset_loader
