"""
Time Manager
Handles game time simulation including day/night cycles
"""

from settings import (
    DAY_START, NIGHT_START, SECONDS_PER_GAME_MINUTE, 
    SECONDS_PER_GAME_HOUR, TOTAL_DAYS
)


class TimeManager:
    """Manages game time and day/night cycles"""
    
    def __init__(self):
        """Initialize time manager"""
        self.current_hour = DAY_START  # Start at 8 AM
        self.current_minute = 0
        self.current_day = 1
        self.elapsed_seconds = 0
        
    def update(self, delta_time):
        """Update game time based on real time passed"""
        self.elapsed_seconds += delta_time
        
        # Convert real seconds to game time
        game_minutes = self.elapsed_seconds / SECONDS_PER_GAME_MINUTE
        self.current_minute += game_minutes
        self.elapsed_seconds = 0
        
        # Handle hour rollovers
        if self.current_minute >= 60:
            hours_added = int(self.current_minute / 60)
            self.current_hour += hours_added
            self.current_minute = self.current_minute % 60
        
        # Handle day rollovers (24-hour clock)
        if self.current_hour >= 24:
            self.current_hour = self.current_hour % 24
            # Note: day increment is handled by GameState
    
    def is_night(self):
        """Check if current time is night (20:00 - 07:59)"""
        return self.current_hour >= NIGHT_START or self.current_hour < DAY_START
    
    def is_day(self):
        """Check if current time is day (08:00 - 19:59)"""
        return not self.is_night()
    
    def get_time_string(self):
        """Return formatted time string HH:MM"""
        return f"{int(self.current_hour):02d}:{int(self.current_minute):02d}"
    
    def day_complete(self):
        """Check if the day has completed (passed midnight)"""
        # This is checked when time wraps from 23:59 to 00:00
        return self.current_hour < DAY_START and self.elapsed_seconds == 0
    
    def reset_day(self):
        """Reset time to start of next day"""
        self.current_hour = DAY_START
        self.current_minute = 0
        self.elapsed_seconds = 0
    
    def get_day(self):
        """Get current day number"""
        return self.current_day
    
    def get_hour(self):
        """Get current hour (0-23)"""
        return int(self.current_hour)
    
    def get_minute(self):
        """Get current minute (0-59)"""
        return int(self.current_minute)
    
    def get_progress_day_percent(self):
        """Get percentage of day completed (0-100)"""
        # From 8 AM to next 8 AM is 24 hours
        total_minutes = 24 * 60
        current_minutes = (self.current_hour - DAY_START) * 60 + self.current_minute
        
        if current_minutes < 0:
            current_minutes += 24 * 60
        
        return (current_minutes / total_minutes) * 100
