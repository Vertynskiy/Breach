"""
Управления экранами игры
Обрабатывает переключение между 5 основными экранами
"""

import pygame
from enum import Enum


class ScreenType(Enum):
    """Типы экранов в игре"""
    MAIN_MENU = 1
    OBSERVATION = 2  # Главное наблюдение
    CONTROL_PANEL = 3  # Панель управления
    MONITORS = 4  # Аномальные мониторы
    LABORATORY = 5  # Лаборатория
    JOURNAL = 6  # Журнал
    GAME_OVER = 7


class ScreenManager:
    """Управляет экранами пользовательского интерфейса"""
    
    def __init__(self, game_state):
        """Инициализация менеджера экранов"""
        self.game_state = game_state
        self.current_screen = ScreenType.OBSERVATION
        self.previous_screen = ScreenType.OBSERVATION
        
        # Плейсхолдеры для экранов (будут реальные классы)
        self.screens = {
            ScreenType.OBSERVATION: ObservationScreen(game_state),
            ScreenType.CONTROL_PANEL: ControlPanelScreen(game_state),
            ScreenType.MONITORS: MonitorsScreen(game_state),
            ScreenType.LABORATORY: LaboratoryScreen(game_state),
            ScreenType.JOURNAL: JournalScreen(game_state),
        }
    
    def switch_screen(self, screen_type):
        """Переключиться на другой экран"""
        if screen_type in self.screens:
            self.previous_screen = self.current_screen
            self.current_screen = screen_type
    
    def handle_event(self, event):
        """Обработать событие пользователя"""
        if event.type == pygame.KEYDOWN:
            # Переключение между экранами по цифрам 1-6
            key_map = {
                pygame.K_1: ScreenType.OBSERVATION,
                pygame.K_2: ScreenType.CONTROL_PANEL,
                pygame.K_3: ScreenType.MONITORS,
                pygame.K_4: ScreenType.LABORATORY,
                pygame.K_5: ScreenType.JOURNAL,
            }
            if event.key in key_map:
                self.switch_screen(key_map[event.key])
        
        # Передать событие текущему экрану
        if self.current_screen in self.screens:
            self.screens[self.current_screen].handle_event(event)
    
    def update(self):
        """Обновить текущий экран"""
        if self.current_screen in self.screens:
            self.screens[self.current_screen].update(self.game_state)
    
    def render(self, surface):
        """Отрисовать текущий экран"""
        if self.current_screen in self.screens:
            self.screens[self.current_screen].render(surface)


class BaseScreen:
    """Базовый класс для всех экранов"""
    
    def __init__(self, game_state):
        self.game_state = game_state
    
    def handle_event(self, event):
        """Обработать событие - переопределить в подклассе"""
        pass
    
    def update(self, game_state):
        """Обновить логику - переопределить в подклассе"""
        pass
    
    def render(self, surface):
        """Отрисовать экран - переопределить в подклассе"""
        pass


class ObservationScreen(BaseScreen):
    """Экран главного наблюдения"""
    
    def render(self, surface):
        from settings import COLOR_DARK_GRAY, COLOR_WHITE
        surface.fill(COLOR_DARK_GRAY)
        # Простой текст для отладки
        font = pygame.font.Font(None, 36)
        text = font.render("OBSERVATION ROOM", True, COLOR_WHITE)
        surface.blit(text, (50, 50))


class ControlPanelScreen(BaseScreen):
    """Экран панели управления"""
    
    def render(self, surface):
        from settings import COLOR_DARK_GRAY, COLOR_WHITE
        surface.fill(COLOR_DARK_GRAY)
        font = pygame.font.Font(None, 36)
        text = font.render("CONTROL PANEL", True, COLOR_WHITE)
        surface.blit(text, (50, 50))


class MonitorsScreen(BaseScreen):
    """Экран мониторов аномалий (FNAF-style)"""
    
    def render(self, surface):
        from settings import COLOR_DARK_GRAY, COLOR_WHITE
        surface.fill(COLOR_DARK_GRAY)
        font = pygame.font.Font(None, 36)
        text = font.render("ANOMALY MONITORS", True, COLOR_WHITE)
        surface.blit(text, (50, 50))


class LaboratoryScreen(BaseScreen):
    """Экран лаборатории"""
    
    def render(self, surface):
        from settings import COLOR_DARK_GRAY, COLOR_WHITE
        surface.fill(COLOR_DARK_GRAY)
        font = pygame.font.Font(None, 36)
        text = font.render("LABORATORY", True, COLOR_WHITE)
        surface.blit(text, (50, 50))


class JournalScreen(BaseScreen):
    """Экран журнала и архива"""
    
    def render(self, surface):
        from settings import COLOR_DARK_GRAY, COLOR_WHITE
        surface.fill(COLOR_DARK_GRAY)
        font = pygame.font.Font(None, 36)
        text = font.render("JOURNAL & ARCHIVE", True, COLOR_WHITE)
        surface.blit(text, (50, 50))
