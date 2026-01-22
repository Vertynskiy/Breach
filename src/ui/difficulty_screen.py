"""
Difficulty Selection Screen for Breach
Player selects game difficulty
"""
import pygame
from src.ui.ui_elements import Button, TextDisplay, Panel
from src.assets.asset_loader import get_asset_loader
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GREEN, COLOR_YELLOW


class DifficultyScreen:
    """Difficulty selection screen"""

    def __init__(self, on_start_callback):
        """Initialize difficulty selection

        on_start_callback: function that takes difficulty as parameter
        """
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 20)
        self.info_font = pygame.font.Font(None, 16)

        # Загрузи фон (тот же фон, что и главное меню, но можно другой)
        asset_loader = get_asset_loader()
        self.bg_texture = asset_loader.load('bg_main_menu')
        if self.bg_texture is None:
            self.bg_texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_texture.fill((20, 20, 30))

        # State
        self.selected_difficulty = 'normal'  # normal, hard, insane
        self.on_start_callback = on_start_callback

        # Difficulty panels
        self.difficulty_panels = {
            'normal': Panel(100, 250, 300, 200, "NORMAL"),
            'hard': Panel(490, 250, 300, 200, "HARD"),
            'insane': Panel(880, 250, 300, 200, "INSANE"),
        }

        # Start button
        self.start_button = Button(400, 550, 400, 60, "START GAME",
                                   self._on_start_clicked)

        # Info text for each difficulty
        self.info_displays = {
            'normal': [
                "BALANCED",
                "Resource: 1.0x",
                "Events: 5.5/day",
                "Recommended"
            ],
            'hard': [
                "CHALLENGING",
                "Resource: 1.2x",
                "Events: 7/day",
                "Experienced"
            ],
            'insane': [
                "EXTREME",
                "Resource: 1.4x",
                "Events: 9/day",
                "Hardcore"
            ],
        }

    def _on_start_clicked(self):
        """Called when start button is clicked"""
        if self.on_start_callback:
            self.on_start_callback(self.selected_difficulty)

    def handle_event(self, event):
        """Handle user input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check difficulty panel clicks
            for diff, panel in self.difficulty_panels.items():
                if panel.rect.collidepoint(event.pos):
                    self.selected_difficulty = diff

            # Check start button
            self.start_button.handle_event(event)

        elif event.type == pygame.KEYDOWN:
            # Arrow keys to select difficulty
            difficulties = ['normal', 'hard', 'insane']
            current_idx = difficulties.index(self.selected_difficulty)

            if event.key == pygame.K_LEFT:
                self.selected_difficulty = difficulties[(current_idx - 1) % 3]
            elif event.key == pygame.K_RIGHT:
                self.selected_difficulty = difficulties[(current_idx + 1) % 3]
            elif event.key == pygame.K_RETURN:
                self._on_start_clicked()

    def update(self, game_state):
        """Update menu state"""
        pass

    def render(self, surface):
        """Render menu"""
        # Background
        surface.blit(self.bg_texture, (0, 0))

        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Title
        title_surf = self.title_font.render("SELECT DIFFICULTY", True, COLOR_GREEN)
        surface.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 30))

        # Subtitle
        subtitle_surf = self.subtitle_font.render("Choose your challenge", True, COLOR_WHITE)
        surface.blit(subtitle_surf, (SCREEN_WIDTH // 2 - subtitle_surf.get_width() // 2, 120))

        # Draw difficulty panels
        for diff, panel in self.difficulty_panels.items():
            panel.render(surface)

            # Highlight selected difficulty with green border
            if diff == self.selected_difficulty:
                pygame.draw.rect(surface, COLOR_GREEN, panel.rect, 5)

            # Draw info text inside panels
            info_text = self.info_displays[diff]
            y_offset = panel.rect.y + 40
            for line in info_text:
                line_surf = self.info_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (panel.rect.x + 15, y_offset))
                y_offset += 35

        # Start button
        self.start_button.render(surface)

        # Instructions
        instructions = self.font.render("ARROW KEYS: Select | ENTER: Start | MOUSE: Click", True, COLOR_YELLOW)
        surface.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 40))
