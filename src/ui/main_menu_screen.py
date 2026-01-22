"""
Main Menu Screen for Breach
Beautiful start menu with game title and navigation
"""
import pygame
from src.ui.ui_elements import Button, TextDisplay, Panel
from src.assets.asset_loader import get_asset_loader
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GREEN, COLOR_YELLOW


class MainMenuScreen:
    """Beautiful main menu screen"""

    def __init__(self, on_new_game_callback, on_exit_callback):
        """Initialize main menu

        on_new_game_callback: функция при нажатии "NEW GAME"
        on_exit_callback: функция при нажатии "EXIT"
        """
        self.on_new_game_callback = on_new_game_callback
        self.on_exit_callback = on_exit_callback

        # Загрузи фон
        asset_loader = get_asset_loader()
        self.bg_texture = asset_loader.load('bg_main_menu')
        if self.bg_texture is None:
            self.bg_texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_texture.fill((20, 20, 30))

        # Шрифты
        self.title_font = pygame.font.Font(None, 120)  # Большой для названия
        self.subtitle_font = pygame.font.Font(None, 40)  # Подзаголовок
        self.button_font = pygame.font.Font(None, 32)  # Кнопки
        self.small_font = pygame.font.Font(None, 20)  # Мелкий текст

        # Кнопки меню
        # Кнопка "NEW GAME"
        self.btn_new_game = Button(
            SCREEN_WIDTH // 2 - 150, 350, 300, 70, "NEW GAME",
            self._on_new_game_clicked
        )

        # Кнопка "EXIT"
        self.btn_exit = Button(
            SCREEN_WIDTH // 2 - 150, 500, 300, 70, "EXIT",
            self._on_exit_clicked
        )

        # Эффект для кнопок
        self.button_glow = 0
        self.glow_direction = 1

    def _on_new_game_clicked(self):
        """Callback when NEW GAME is clicked"""
        if self.on_new_game_callback:
            self.on_new_game_callback()

    def _on_exit_clicked(self):
        """Callback when EXIT is clicked"""
        if self.on_exit_callback:
            self.on_exit_callback()

    def handle_event(self, event):
        """Handle user input"""
        self.btn_new_game.handle_event(event)
        self.btn_exit.handle_event(event)

    def update(self, game_state):
        """Update menu state"""
        # Эффект свечения для кнопок
        self.button_glow += 0.5 * self.glow_direction
        if self.button_glow > 30:
            self.glow_direction = -1
        elif self.button_glow < 0:
            self.glow_direction = 1

    def render(self, surface):
        """Render main menu"""
        # Фон
        surface.blit(self.bg_texture, (0, 0))

        # Полупрозрачный слой поверх фона (затемнение)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Название игры - "BREACH"
        title_text = "BREACH"
        title_surf = self.title_font.render(title_text, True, COLOR_GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))

        # Эффект свечения вокруг текста
        for i in range(3):
            glow_surf = self.title_font.render(title_text, True, (0, 100, 150))
            glow_surf.set_alpha(50 - i * 15)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
            surface.blit(glow_surf, glow_rect)

        surface.blit(title_surf, title_rect)

        # Подзаголовок - "Management Horror Game"
        subtitle_text = "Management Horror Game"
        subtitle_surf = self.subtitle_font.render(subtitle_text, True, COLOR_WHITE)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 170))
        surface.blit(subtitle_surf, subtitle_rect)

        # Линия под названием (для красоты)
        pygame.draw.line(surface, COLOR_GREEN,
                         (SCREEN_WIDTH // 2 - 300, 220),
                         (SCREEN_WIDTH // 2 + 300, 220), 3)

        # Небольшая информация
        info_text = "Watch the forest. Keep your sanity. Survive the anomalies."
        info_surf = self.small_font.render(info_text, True, COLOR_YELLOW)
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, 260))
        surface.blit(info_surf, info_rect)

        # Кнопки
        self.btn_new_game.render(surface)
        self.btn_exit.render(surface)

        # Версия в углу
        version_text = "v0.1 Alpha"
        version_surf = self.small_font.render(version_text, True, (100, 100, 100))
        surface.blit(version_surf, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))
