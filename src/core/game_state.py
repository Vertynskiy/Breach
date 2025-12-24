"""
Game State Manager
Manages overall game state including resources, time, sanity, and difficulty
"""

from datetime import datetime
from src.core.resource_manager import ResourceManager
from src.core.sanity_system import SanitySystem
from src.core.time_manager import TimeManager
from src.core.event_generator import EventGenerator
from settings import TOTAL_DAYS, DIFFICULTIES


class GameState:
    """Main game state manager"""
    
    def __init__(self, difficulty='normal'):
        """Initialize game state"""
        self.difficulty = difficulty
        self.current_day = 1
        self.game_over = False
        self.ending_type = None  # 'survival', 'compromise', 'failure'
        
        # Initialize subsystems
        self.time_manager = TimeManager()
        self.resource_manager = ResourceManager(difficulty)
        self.sanity_system = SanitySystem(difficulty)
        self.event_generator = EventGenerator(difficulty)
        
        # Game tracking
        self.events_triggered = []
        self.choices_made = []
        self.director_logs_found = []
        self.anomalies_observed = []
        
    def update(self, delta_time):
        """Update game state each frame"""
        if self.game_over:
            return
        
        # Update time
        self.time_manager.update(delta_time)
        
        # Update resources based on current time period
        self.resource_manager.update(self.time_manager.is_night(), delta_time)
        
        # Update sanity based on environment
        sanity_delta = 0
        if self.time_manager.is_night():
            sanity_delta -= 0.5  # Isolation penalty
        if not self.resource_manager.has_light():
            sanity_delta -= 1.0  # Darkness penalty
        
        self.sanity_system.update(sanity_delta)
        
        # Check for critical conditions
        if self.resource_manager.is_critical('fuel'):
            self.game_over = True
            self.ending_type = 'failure'
        
        if self.sanity_system.is_fractured():
            self.game_over = True
            self.ending_type = 'failure'
        
        # Check day completion
        if self.time_manager.day_complete():
            self.complete_day()
    
    def complete_day(self):
        """Handle end of day logic"""
        self.current_day += 1
        
        if self.current_day > TOTAL_DAYS:
            self.game_over = True
            self.ending_type = 'survival'  # Placeholder
        else:
            self.time_manager.reset_day()
    
    def trigger_event(self, event):
        """Record triggered event"""
        self.events_triggered.append({
            'day': self.current_day,
            'time': self.time_manager.get_time_string(),
            'event': event
        })
        
        # Apply event effects
        if 'sanity' in event:
            self.sanity_system.modify(event['sanity'])
        if 'resources' in event:
            for resource, amount in event['resources'].items():
                self.resource_manager.modify(resource, amount)
    
    def get_status(self):
        """Get current game status"""
        return {
            'day': self.current_day,
            'time': self.time_manager.get_time_string(),
            'is_night': self.time_manager.is_night(),
            'resources': self.resource_manager.get_all(),
            'sanity': self.sanity_system.get_level(),
            'sanity_state': self.sanity_system.get_state(),
            'game_over': self.game_over,
            'ending': self.ending_type
        }
    
    def save_game(self, filename):
        """Save game state to file"""
        # Implemented in save_system.py
        pass
    
    def load_game(self, filename):
        """Load game state from file"""
        # Implemented in save_system.py
        pass
