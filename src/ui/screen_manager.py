"""
Screen Manager for Breach game
Manages switching between 5 game screens
"""

import pygame
from enum import Enum
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_DARK_GRAY, COLOR_WHITE, COLOR_GREEN
from src.ui.ui_elements import Button, TextDisplay, Panel, StatusBar
from src.assets.texture_generator import get_texture_generator
from src.ui.menu_screen import MainMenuScreen

class ScreenType(Enum):
    """Screen types in the game"""
    MAIN_MENU = 0
    MAIN_MENU = 1
    OBSERVATION = 2  # Main observation room
    CONTROL_PANEL = 3  # Control panel
    MONITORS = 4  # Anomaly monitors
    LABORATORY = 5  # Laboratory
    JOURNAL = 6  # Journal & archive
    GAME_OVER = 7


class BaseScreen:
    """Base class for all screens"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.bg_texture = get_texture_generator().generate_screen_background(
            SCREEN_WIDTH, SCREEN_HEIGHT
        )

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
    """Main observation room screen"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 24)

        # Create UI elements
        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)
        self.main_panel = Panel(50, 100, 600, 600, "OBSERVATION ROOM")

        # Status bars
        self.fuel_bar = StatusBar(100, 150, 400, 20, "Fuel", (255, 220, 50))
        self.power_bar = StatusBar(100, 200, 400, 20, "Power", (50, 220, 50))
        self.sanity_bar = StatusBar(100, 250, 400, 20, "Sanity", (220, 50, 50))

        # Info text
        self.time_display = TextDisplay(750, 150, "Time: 08:00", 20, COLOR_WHITE)
        self.day_display = TextDisplay(750, 200, "Day: 1/20", 20, COLOR_WHITE)
        self.status_display = TextDisplay(750, 250, "Status: Stable", 20, COLOR_GREEN)

    def update(self, game_state):
        """Update observation screen"""
        status = game_state.get_status()

        # Update bars
        self.fuel_bar.set_value(status['resources']['fuel'], 100)
        self.sanity_bar.set_value(status['sanity'], 100)

        # Update text
        self.time_display.update(f"Time: {status['time']}")
        self.day_display.update(f"Day: {status['day']}/20")
        self.status_display.update(f"Status: {status['sanity_state']}")

    def render(self, surface):
        """Render observation screen"""
        super().render(surface)

        # Draw title bar
        surface.blit(self.title_bar, (0, 0))

        # Draw title
        title_surf = self.title_font.render("OBSERVATION ROOM", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))

        # Draw panels
        self.main_panel.render(surface)

        # Draw status bars
        self.fuel_bar.render(surface)
        self.power_bar.render(surface)
        self.sanity_bar.render(surface)

        # Draw info
        self.time_display.render(surface)
        self.day_display.render(surface)
        self.status_display.render(surface)


class ControlPanelScreen(BaseScreen):
    """Control panel screen"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 20)

        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)
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

        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)
        self.main_panel = Panel(50, 100, 900, 600, "ANOMALY MONITORS")

        # Camera feeds (4 monitors)
        self.monitors = [
            Panel(100, 180, 350, 280, "Corridor"),
            Panel(520, 180, 350, 280, "Engine Room"),
            Panel(100, 500, 350, 140, "Entrance"),
            Panel(520, 500, 350, 140, "Roof"),
        ]

        self.battery_display = TextDisplay(100, 650, "Battery: 45%", 16, COLOR_YELLOW := (255, 220, 50))

    def render(self, surface):
        """Render monitors screen"""
        super().render(surface)

        surface.blit(self.title_bar, (0, 0))
        title_surf = self.title_font.render("ANOMALY MONITORS", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))

        self.main_panel.render(surface)
        for monitor in self.monitors:
            monitor.render(surface)
        self.battery_display.render(surface)


class LaboratoryScreen(BaseScreen):
    """Laboratory screen with mini-games"""

    def __init__(self, game_state):
        super().__init__(game_state)
        self.title_font = pygame.font.Font(None, 48)

        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)
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

        self.title_bar = get_texture_generator().generate_title_bar(SCREEN_WIDTH, 60)
        self.main_panel = Panel(50, 100, 900, 600, "JOURNAL & ARCHIVE")

        # Journal sections
        self.duty_log_panel = Panel(100, 180, 270, 250, "Duty Log")
        self.personal_notes_panel = Panel(420, 180, 270, 250, "Personal Notes")
        self.director_logs_panel = Panel(740, 180, 150, 250, "Director's Logs")
        self.anomaly_map_panel = Panel(100, 480, 790, 180, "Anomaly Map")

        # Log counter
        self.log_count = TextDisplay(100, 680, "Logs Found: 2/20", 16, COLOR_WHITE)

    def render(self, surface):
        """Render journal screen"""
        super().render(surface)

        surface.blit(self.title_bar, (0, 0))
        title_surf = self.title_font.render("JOURNAL & ARCHIVE", True, COLOR_GREEN)
        surface.blit(title_surf, (30, 10))

        self.main_panel.render(surface)
        self.duty_log_panel.render(surface)
        self.personal_notes_panel.render(surface)
        self.director_logs_panel.render(surface)
        self.anomaly_map_panel.render(surface)
        self.log_count.render(surface)


class ScreenManager:
    """Manages all game screens"""

    def __init__(self, game_state):
        """Initialize screen manager"""
        self.game_state = game_state
        self.current_screen = ScreenType.MAIN_MENU  # Начинаем с главного меню!

        # Create all game screens
        self.screens = {
            ScreenType.OBSERVATION: ObservationScreen(game_state),
            ScreenType.CONTROL_PANEL: ControlPanelScreen(game_state),
            ScreenType.MONITORS: MonitorsScreen(game_state),
            ScreenType.LABORATORY: LaboratoryScreen(game_state),
            ScreenType.JOURNAL: JournalScreen(game_state),
        }

        # Create main menu with callback
        self.screens[ScreenType.MAIN_MENU] = MainMenuScreen(self._on_difficulty_selected)

    def _on_difficulty_selected(self, difficulty):
        """Called when player selects difficulty from main menu"""
        # Set game difficulty
        self.game_state.difficulty = difficulty
        # Switch to observation screen to start the game
        self.switch_screen(ScreenType.OBSERVATION)

    def switch_screen(self, screen_type: ScreenType):
        """Switch to another screen"""
        if screen_type in self.screens:
            self.current_screen = screen_type

    def handle_event(self, event):
        """Handle user input"""
        if event.type == pygame.KEYDOWN:
            # Screen switching with number keys
            key_map = {
                pygame.K_1: ScreenType.OBSERVATION,
                pygame.K_2: ScreenType.CONTROL_PANEL,
                pygame.K_3: ScreenType.MONITORS,
                pygame.K_4: ScreenType.LABORATORY,
                pygame.K_5: ScreenType.JOURNAL,
                pygame.K_0: ScreenType.MAIN_MENU,  # Можно вернуться на меню нажатием 0

            }
            if event.key in key_map:
                self.switch_screen(key_map[event.key])

        # Pass event to current screen
        if self.current_screen in self.screens:
            self.screens[self.current_screen].handle_event(event)

    def update(self):
        """Update current screen"""
        if self.current_screen in self.screens:
            self.screens[self.current_screen].update(self.game_state)

    def render(self, surface):
        """Render current screen"""
        if self.current_screen in self.screens:
            self.screens[self.current_screen].render(surface)
