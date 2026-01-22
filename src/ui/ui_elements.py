"""
UI Elements for Breach game
Enhanced with proper rendering
"""
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GREEN, COLOR_YELLOW


class TextDisplay:
    """Text display element"""

    def __init__(self, x: int, y: int, text: str, size: int = 18, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font(None, size)

    def update(self, text: str):
        """Update text"""
        self.text = text

    def render(self, surface):
        """Render text"""
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, (self.x, self.y))


class StatusBar:
    """Status bar with value indicator"""

    def __init__(self, x: int, y: int, width: int, height: int, label: str = "", color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.color = color
        self.current_value = 100
        self.max_value = 100
        self.font = pygame.font.Font(None, 16)

    def set_value(self, current: float, max_val: float):
        """Set bar value"""
        self.current_value = current
        self.max_value = max_val

    def render(self, surface):
        """Render status bar"""
        # Background
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))

        # Border
        pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height), 2)

        # Value bar
        if self.max_value > 0:
            value_width = (self.current_value / self.max_value) * self.width
        else:
            value_width = 0

        pygame.draw.rect(surface, self.color, (self.x, self.y, value_width, self.height))

        # Label
        if self.label:
            label_surf = self.font.render(self.label, True, (255, 255, 255))
            surface.blit(label_surf, (self.x + 5, self.y + 2))


class Panel:
    """UI Panel element"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 24)

        # Цвета для панели
        self.bg_color = (20, 35, 60)  # Тёмный синий
        self.border_color = (0, 150, 200)  # Светлый голубой
        self.border_width = 2

    def render(self, surface):
        """Render panel"""
        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        # Title
        if self.title:
            title_surf = self.font.render(self.title, True, (0, 200, 255))
            surface.blit(title_surf, (self.x + 10, self.y + 10))


class Button:
    """Interactive button element"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str = "", callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 20)
        self.hovered = False
        self.pressed = False

        # Цвета
        self.normal_color = (20, 100, 160)
        self.hover_color = (30, 130, 190)
        self.pressed_color = (15, 80, 130)
        self.border_color = (0, 150, 220)
        self.current_color = self.normal_color

    def handle_event(self, event):
        """Handle user input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                if self.callback:
                    self.callback()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False

        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

    def update(self):
        """Update button state"""
        if self.pressed:
            self.current_color = self.pressed_color
        elif self.hovered:
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color

    def render(self, surface):
        """Render button"""
        self.update()

        # Background
        pygame.draw.rect(surface, self.current_color, self.rect)

        # Border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        # Highlight on top (3D effect)
        pygame.draw.line(surface, (100, 200, 255),
                        (self.x + 5, self.y + 5),
                        (self.x + self.width - 5, self.y + 5), 2)

        # Text
        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
