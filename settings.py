# Game Settings and Constants
# Breach - Management Horror

import pygame

# ========== SCREEN SETTINGS ==========
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# ========== COLORS ==========
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_GRAY = (40, 40, 40)
COLOR_GRAY = (128, 128, 128)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_RED = (220, 50, 50)
COLOR_GREEN = (50, 220, 50)
COLOR_BLUE = (50, 100, 220)
COLOR_YELLOW = (255, 220, 50)
COLOR_ORANGE = (255, 140, 50)
COLOR_PURPLE = (180, 100, 220)
COLOR_CYAN = (50, 200, 200)

# ========== GAME TIME ==========
TOTAL_DAYS = 20
DAY_START = 8  # 08:00
NIGHT_START = 20  # 20:00
SECONDS_PER_GAME_MINUTE = 0.5  # 1 real second = 2 game minutes
SECONDS_PER_GAME_HOUR = 30  # 30 real seconds = 1 game hour

# ========== RESOURCE SETTINGS ==========
# Format: (max_amount, day_consumption, night_consumption, critical_level)
RESOURCES = {
    'fuel': {
        'max': 100,
        'normal': {'day': -2.5, 'night': -6.0},
        'hard': {'day': -3.0, 'night': -7.5},
        'insane': {'day': -4.0, 'night': -10.0},
        'critical': 15
    },
    'food': {
        'max': 50,
        'normal': {'day': -0.3, 'night': 0},
        'hard': {'day': -0.5, 'night': 0},
        'insane': {'day': -0.8, 'night': 0},
        'critical': 5
    },
    'water': {
        'max': 50,
        'normal': {'day': -0.25, 'night': 0},
        'hard': {'day': -0.4, 'night': 0},
        'insane': {'day': -0.6, 'night': 0},
        'critical': 5
    },
    'parts': {
        'max': 30,
        'normal': {'day': 0, 'night': 0},
        'hard': {'day': 0, 'night': 0},
        'insane': {'day': 0, 'night': 0},
        'critical': 2
    },
    'batteries': {
        'max': 20,
        'normal': {'day': 0, 'night': -0.5},
        'hard': {'day': 0, 'night': -0.667},
        'insane': {'day': 0, 'night': -1.0},
        'critical': 1
    }
}

SPECIAL_RESOURCES = {
    'sedatives': {'max': 10, 'sanity_effect': -30},
    'isotopes': {'max': 8, 'sensor_bonus': 5},
    'director_logs': {'max': 20}
}

# ========== SANITY SETTINGS ==========
SANITY_RANGES = {
    'stable': (0, 30),
    'anxious': (31, 60),
    'panicked': (61, 80),
    'fractured': (81, 100)
}

SANITY_MODIFIERS = {
    'darkness': -1.0,  # per minute
    'isolation': -0.5,  # per minute
    'event_minor': -5,
    'event_moderate': -15,
    'event_severe': -30,
    'log_finding': {'sad': -5, 'neutral': 0, 'informative': 10, 'horrifying': -15},
    'reading_logs': 1.0,  # per minute
    'sedative': -30  # one-time
}

FRACTURED_TIMEOUT = 600  # 10 minutes at sanity 100 = GAME OVER

# ========== DIFFICULTY SETTINGS ==========
DIFFICULTIES = {
    'normal': {
        'resource_multiplier': 1.0,
        'event_frequency': 5.5,  # events per day
        'anomaly_event_chance': 0.30,
        'sanity_penalty_mult': 1.0,
        'starting_sanity': 50
    },
    'hard': {
        'resource_multiplier': 1.2,
        'event_frequency': 7.0,
        'anomaly_event_chance': 0.50,
        'sanity_penalty_mult': 1.2,
        'starting_sanity': 45
    },
    'insane': {
        'resource_multiplier': 1.4,
        'event_frequency': 9.0,
        'anomaly_event_chance': 0.85,
        'sanity_penalty_mult': 1.5,
        'starting_sanity': 40
    }
}

# ========== EQUIPMENT REPAIR COSTS ==========
REPAIR_COSTS = {
    'normal': {'generator': 5, 'heating': 3, 'ventilation': 3, 'lighting': 2},
    'hard': {'generator': 6, 'heating': 4, 'ventilation': 4, 'lighting': 3},
    'insane': {'generator': 8, 'heating': 6, 'ventilation': 5, 'lighting': 4}
}

# ========== MINI-GAME SETTINGS ==========
SPECTROMETER_DIFFICULTY = 4  # Number of peaks to match
MORSE_CODE_LENGTH = 8  # Characters in morse code puzzle

# ========== TEXTURE PATHS ==========
TEXTURE_PATHS = {
    'ui': 'assets/textures/ui/',
    'environment': 'assets/textures/environment/',
    'objects': 'assets/textures/objects/',
    'anomalies': 'assets/textures/anomalies/'
}

# ========== FONT PATHS ==========
FONT_PATHS = {
    'title': 'assets/fonts/title.ttf',
    'body': 'assets/fonts/body.ttf',
    'mono': 'assets/fonts/mono.ttf'
}

# ========== SOUND PATHS ==========
SOUND_PATHS = {
    'ambient': 'assets/audio/ambient/',
    'events': 'assets/audio/events/',
    'ui': 'assets/audio/ui/'
}
