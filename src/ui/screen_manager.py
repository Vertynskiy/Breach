"""
Screen Manager for Breach game
Manages switching between game screens
"""
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_DARK_GRAY, COLOR_WHITE, COLOR_GREEN
from enum import Enum
from src.ui.ui_elements import Button, TextDisplay, Panel, StatusBar
from src.assets.texture_generator import get_texture_generator
from src.ui.main_menu_screen import MainMenuScreen
from src.ui.difficulty_screen import DifficultyScreen


class ScreenType(Enum):
    """Screen types in the game"""
    MAIN_MENU = 0      # Главное меню
    DIFFICULTY = 1     # Выбор сложности
    OBSERVATION = 2    # Main observation room
    CONTROL_PANEL = 3  # Control panel
    MONITORS = 4       # Anomaly monitors
    LABORATORY = 5     # Laboratory
    JOURNAL = 6        # Journal & archive
    GAME_OVER = 7


class BaseScreen:
    """Base class for all screens"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.bg_texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_texture.fill((20, 20, 30))

    def handle_event(self, event):
        """Handle event - override in subclass"""
        pass

    def update(self, game_state):
        """Update logic - override in subclass"""
        pass

    def render(self, surface):
        """Render screen - override in subclass"""
        surface.blit(self.bg_texture, (0, 0))


class ObservationScreen(BaseScreen):
    """Main observation room screen with window view"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)

        # Create UI elements
        self.title_bar = pygame.Surface((SCREEN_WIDTH, 60))
        self.title_bar.fill((30, 30, 50))

        self.main_panel = Panel(50, 100, 1180, 600, "OBSERVATION ROOM")

        # Window view area (large central area)
        self.window_rect = pygame.Rect(70, 130, 800, 550)

        # Status bars (right side)
        self.fuel_bar = StatusBar(900, 180, 250, 20, "Fuel", (255, 220, 50))
        self.power_bar = StatusBar(900, 240, 250, 20, "Power", (50, 220, 50))
        self.sanity_bar = StatusBar(900, 300, 250, 20, "Sanity", (220, 50, 50))
        self.food_bar = StatusBar(900, 360, 250, 20, "Food", (150, 100, 50))
        self.water_bar = StatusBar(900, 420, 250, 20, "Water", (50, 150, 220))

        # Info text
        self.time_display = TextDisplay(900, 150, "Time: 08:00", 18, COLOR_WHITE)
        self.day_display = TextDisplay(900, 500, "Day: 1/20", 18, COLOR_WHITE)
        self.status_display = TextDisplay(900, 530, "Status: Stable", 18, COLOR_GREEN)

        self.current_view = 'forest'

        # Hint text
        self.hint_text = TextDisplay(70, 690, "Press 1-5 to switch screens", 14, COLOR_WHITE)

    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            # Switch views with arrow keys
            if event.key == pygame.K_UP:
                if self.current_view == 'forest':
                    self.current_view = 'control_room'
                elif self.current_view == 'control_room':
                    self.current_view = 'table'
                else:
                    self.current_view = 'forest'
            elif event.key == pygame.K_DOWN:
                if self.current_view == 'forest':
                    self.current_view = 'table'
                elif self.current_view == 'table':
                    self.current_view = 'control_room'
                else:
                    self.current_view = 'forest'

    def update(self, game_state):
        """Update observation screen"""
        status = game_state.get_status()

        # Update bars with actual values
        self.fuel_bar.set_value(status['resources']['fuel'], 100)
        self.power_bar.set_value(status['resources']['batteries'], 20)
        self.sanity_bar.set_value(status['sanity'], 100)
        self.food_bar.set_value(status['resources']['food'], 50)
        self.water_bar.set_value(status['resources']['water'], 50)

        # Update text
        self.time_display.update(f"Time: {status['time']}")
        self.day_display.update(f"Day: {status['day']}/20")

        # Sanity state with color
        sanity_state = status['sanity_state']
        sanity_color = COLOR_GREEN
        if sanity_state == 'anxious':
            sanity_color = (255, 255, 0)
        elif sanity_state == 'panicked':
            sanity_color = (255, 140, 0)
        elif sanity_state == 'fractured':
            sanity_color = (220, 50, 50)

        self.status_display.color = sanity_color
        self.status_display.update(f"Status: {sanity_state.upper()}")

    def render(self, surface):
        """Render observation screen"""
        super().render(surface)

        # Draw title bar
        surface.blit(self.title_bar, (0, 0))

        # Draw title
        title_surf = self.title_font.render("OBSERVATION ROOM", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))

        # Draw main panel
        self.main_panel.render(surface)

        # Draw window with simple view
        pygame.draw.rect(surface, (100, 100, 100), self.window_rect, 2)
        pygame.draw.rect(surface, (40, 60, 80), self.window_rect)

        # Draw status bars
        self.fuel_bar.render(surface)
        self.power_bar.render(surface)
        self.sanity_bar.render(surface)
        self.food_bar.render(surface)
        self.water_bar.render(surface)

        # Draw info
        self.time_display.render(surface)
        self.day_display.render(surface)
        self.status_display.render(surface)

        # Draw view label
        view_label = self.small_font.render(f"View: {self.current_view.upper()}", True, (255, 255, 0))
        surface.blit(view_label, (70, 695))

        # Draw hint
        self.hint_text.render(surface)


class ControlPanelScreen(BaseScreen):
    """Control panel screen"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 20)
        self.title_bar = pygame.Surface((SCREEN_WIDTH, 60))
        self.title_bar.fill((30, 30, 50))

        self.main_panel = Panel(50, 100, 900, 600, "CONTROL PANEL")

        # Generator controls
        self.power_mode_display = TextDisplay(150, 180, "Power Mode: Normal", 18, COLOR_WHITE)
        self.generator_output = TextDisplay(150, 220, "Output: 85%", 18, COLOR_GREEN)

        # Buttons
        self.power_up_btn = Button(500, 180, 150, 40, "Increase Power", lambda: None)
        self.power_down_btn = Button(680, 180, 150, 40, "Decrease Power", lambda: None)

    def render(self, surface):
        """Render control panel screen"""
        super().render(surface)
        surface.blit(self.title_bar, (0, 0))
        title_surf = self.title_font.render("CONTROL PANEL", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))
        self.main_panel.render(surface)
        self.power_mode_display.render(surface)
        self.generator_output.render(surface)
        self.power_up_btn.render(surface)
        self.power_down_btn.render(surface)


class MonitorsScreen(BaseScreen):
    """Anomaly monitors screen (FNAF-style)"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 14)
        self.title_bar = pygame.Surface((SCREEN_WIDTH, 60))
        self.title_bar.fill((30, 30, 50))

        self.main_panel = Panel(50, 100, 1180, 600, "ANOMALY MONITORS")

        # Camera feeds (4 monitors in grid)
        self.monitors = [
            Panel(70, 140, 540, 260, "Corridor"),
            Panel(640, 140, 540, 260, "Engine Room"),
            Panel(70, 420, 540, 240, "Entrance"),
            Panel(640, 420, 540, 240, "Roof"),
        ]

        # Battery display
        self.battery_display = TextDisplay(70, 680, "Battery: 100%", 16, (255, 255, 0))
        self.hint_text = TextDisplay(70, 710, "UP/DOWN ARROWS: Switch cameras", 14, COLOR_WHITE)

        self.selected_monitor = 0

    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_monitor = (self.selected_monitor - 1) % 4
            elif event.key == pygame.K_DOWN:
                self.selected_monitor = (self.selected_monitor + 1) % 4

    def update(self, game_state):
        """Update monitor screen"""
        status = game_state.get_status()
        battery_pct = (status['resources']['batteries'] / 20) * 100
        self.battery_display.update(f"Battery: {battery_pct:.0f}%")

    def render(self, surface):
        """Render monitors screen"""
        super().render(surface)
        surface.blit(self.title_bar, (0, 0))
        title_surf = self.title_font.render("ANOMALY MONITORS", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))
        self.main_panel.render(surface)

        # Draw all 4 monitors
        for i, monitor in enumerate(self.monitors):
            monitor.render(surface)

            # Highlight selected monitor
            if i == self.selected_monitor:
                pygame.draw.rect(surface, COLOR_GREEN, monitor.rect, 4)

        # Draw battery and hints
        self.battery_display.render(surface)
        self.hint_text.render(surface)


class LaboratoryScreen(BaseScreen):
    """Laboratory screen with mini-games"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.title_bar = pygame.Surface((SCREEN_WIDTH, 60))
        self.title_bar.fill((30, 30, 50))

        self.main_panel = Panel(50, 100, 900, 600, "LABORATORY")

        # Mini-game panels
        self.spectrometer_panel = Panel(100, 180, 250, 250, "Spectrometer")
        self.radio_panel = Panel(420, 180, 250, 250, "Radio")
        self.magnetometer_panel = Panel(740, 180, 150, 250, "Magnetometer")
        self.chemistry_panel = Panel(100, 480, 790, 180, "Chemistry")

        # Info display
        self.isotope_display = TextDisplay(100, 680, "Isotopes: 3/8", 16, COLOR_WHITE)

    def render(self, surface):
        """Render laboratory screen"""
        super().render(surface)
        surface.blit(self.title_bar, (0, 0))
        title_surf = self.title_font.render("LABORATORY", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))
        self.main_panel.render(surface)
        self.spectrometer_panel.render(surface)
        self.radio_panel.render(surface)
        self.magnetometer_panel.render(surface)
        self.chemistry_panel.render(surface)
        self.isotope_display.render(surface)


class JournalScreen(BaseScreen):
    """Journal and archive screen"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 18)
        self.title_bar = pygame.Surface((SCREEN_WIDTH, 60))
        self.title_bar.fill((30, 30, 50))

        self.main_panel = Panel(50, 100, 900, 600, "JOURNAL & ARCHIVE")

        # Journal sections
        self.duty_log_panel = Panel(100, 180, 270, 250, "Duty Log")
        self.personal_notes_panel = Panel(420, 180, 270, 250, "Personal Notes")
        self.director_logs_panel = Panel(740, 180, 150, 250, "Director's Logs")
        self.anomaly_map_panel = Panel(100, 480, 790, 180, "Anomaly Map")

        # Log counter
        self.log_count = TextDisplay(100, 680, "Logs Found: 2/20", 16, COLOR
