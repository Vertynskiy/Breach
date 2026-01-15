"""
View Renderer - Draws different camera views for the observation screens
Procedurally generates windows, forest, tables, control rooms, engines, etc.
"""

import pygame
import random
from typing import Tuple

Color = Tuple[int, int, int]

class ViewRenderer:
    """Renders different views from the research station"""

    def __init__(self):
        self.forest_seed = 12345

    def draw_forest_view(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw window view with forest, sky, and moon"""
        # Sky gradient (dark blue-green night sky)
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(20 * (1 - ratio) + 40 * ratio)
            g = int(30 * (1 - ratio) + 60 * ratio)
            b = int(50 * (1 - ratio) + 100 * ratio)
            pygame.draw.line(surface, (r, g, b),
                           (rect.x, rect.y + y),
                           (rect.x + rect.width, rect.y + y))

        # Stars
        random.seed(self.forest_seed)
        for _ in range(30):
            star_x = rect.x + random.randint(0, rect.width)
            star_y = rect.y + random.randint(0, int(rect.height * 0.4))
            star_brightness = random.randint(100, 255)
            pygame.draw.circle(surface, (star_brightness, star_brightness, star_brightness),
                             (star_x, star_y), 1)

        # Moon
        moon_x = rect.x + rect.width - 80
        moon_y = rect.y + 60
        pygame.draw.circle(surface, (200, 200, 150), (moon_x, moon_y), 40)
        pygame.draw.circle(surface, (220, 220, 200), (moon_x + 10, moon_y + 10), 35)

        # Forest treeline
        tree_base = int(rect.y + rect.height * 0.6)
        pygame.draw.line(surface, (10, 25, 10),
                        (rect.x, tree_base),
                        (rect.x + rect.width, tree_base), 3)

        # Distant trees
        random.seed(self.forest_seed + 1)
        for x in range(rect.x, rect.x + rect.width, 40):
            height = random.randint(50, 120)
            pygame.draw.line(surface, (5, 15, 5),
                           (x + 20, tree_base),
                           (x + 20, tree_base - height), 4)
            points = [(x + 20, tree_base - height),
                     (x, tree_base),
                     (x + 40, tree_base)]
            pygame.draw.polygon(surface, (15, 30, 15), points)

        # Foreground grass
        grass_y = rect.y + rect.height - 30
        pygame.draw.rect(surface, (30, 45, 25),
                        (rect.x, grass_y, rect.width, 30))

        # Window frame
        frame_color = (80, 80, 80)
        pygame.draw.rect(surface, frame_color, rect, 4)
        pygame.draw.line(surface, frame_color,
                        (rect.centerx, rect.y), (rect.centerx, rect.bottom), 2)
        pygame.draw.line(surface, frame_color,
                        (rect.x, rect.centery), (rect.right, rect.centery), 2)

    def draw_table(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw a research table with equipment"""
        # Table surface
        pygame.draw.rect(surface, (60, 50, 40), rect)
        pygame.draw.rect(surface, (100, 80, 60), rect, 3)

        # Table edge highlight
        pygame.draw.line(surface, (80, 70, 60),
                        (rect.x, rect.y), (rect.x + rect.width, rect.y), 2)

        # Monitor on table
        monitor_rect = pygame.Rect(rect.x + 20, rect.y + 20, 80, 50)
        pygame.draw.rect(surface, (30, 30, 40), monitor_rect)
        pygame.draw.rect(surface, (100, 150, 200), monitor_rect, 2)
        pygame.draw.rect(surface, (40, 50, 60),
                       (monitor_rect.x + 5, monitor_rect.y + 5,
                        monitor_rect.width - 10, monitor_rect.height - 12))

        # Documents
        for i in range(3):
            doc_x = rect.x + 120 + i * 35
            doc_y = rect.y + 30
            pygame.draw.rect(surface, (200, 200, 180),
                           (doc_x, doc_y, 30, 40))
            pygame.draw.rect(surface, (150, 150, 140),
                           (doc_x, doc_y, 30, 40), 1)

        # Cup
        cup_rect = pygame.Rect(rect.x + 250, rect.y + 25, 25, 35)
        pygame.draw.ellipse(surface, (100, 80, 60), cup_rect)

    def draw_control_room(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw control room with panels and screens"""
        pygame.draw.rect(surface, (35, 35, 40), rect)

        # Wall panels
        panel_color = (50, 50, 60)
        for row in range(3):
            for col in range(4):
                panel_x = rect.x + col * 60 + 20
                panel_y = rect.y + row * 60 + 30
                pygame.draw.rect(surface, panel_color,
                               (panel_x, panel_y, 50, 50))
                pygame.draw.rect(surface, (100, 100, 120),
                               (panel_x, panel_y, 50, 50), 1)

                # Indicator lights
                pygame.draw.circle(surface, (0, 255, 0),
                                 (panel_x + 12, panel_y + 12), 3)
                pygame.draw.circle(surface, (255, 100, 0),
                                 (panel_x + 38, panel_y + 12), 3)
                pygame.draw.circle(surface, (100, 100, 255),
                                 (panel_x + 25, panel_y + 40), 3)

        # Main console
        console_rect = pygame.Rect(rect.x + 50, rect.y + rect.height - 80, 250, 70)
        pygame.draw.rect(surface, (40, 40, 50), console_rect)
        pygame.draw.
