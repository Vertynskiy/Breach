import random
from settings import DIFFICULTIES


class EventGenerator:
    """Generates random game events"""
    
    # Event templates
    ROUTINE_EVENTS = [
        {'name': 'Generator Fluctuation', 'type': 'routine', 'sanity': -5, 'resources': {'fuel': -5}},
        {'name': 'Equipment Malfunction', 'type': 'routine', 'sanity': -10, 'resources': {'parts': -3}},
        {'name': 'Supply Decay', 'type': 'routine', 'sanity': -3, 'resources': {'food': -5, 'water': -3}},
        {'name': 'System Alert', 'type': 'routine', 'sanity': -5, 'resources': {'batteries': -2}},
    ]
    
    ANOMALOUS_EVENTS = [
        {'name': 'Manifestation Sighting', 'type': 'anomalous', 'sanity': -25, 'resources': {}},
        {'name': 'Sensor Anomaly', 'type': 'anomalous', 'sanity': -15, 'resources': {}},
        {'name': 'Physical Phenomenon', 'type': 'anomalous', 'sanity': -20, 'resources': {}},
    ]
    
    CRITICAL_EVENTS = [
        {'name': "Director's Body Discovery", 'type': 'critical', 'sanity': -40, 'resources': {}},
        {'name': 'Dimensional Breach', 'type': 'critical', 'sanity': -50, 'resources': {}},
        {'name': 'Anomaly Offer', 'type': 'critical', 'sanity': -30, 'resources': {}},
    ]
    
    def __init__(self, difficulty='normal'):
        """Initialize event generator"""
        self.difficulty = difficulty
        diff_config = DIFFICULTIES[difficulty]
        self.event_frequency = diff_config['event_frequency']
        self.anomaly_chance = diff_config['anomaly_event_chance']
        self.events_this_day = 0
    
    def should_trigger_event(self):
        """Check if an event should trigger this hour"""
        # Events per day = frequency, so chance per hour
        chance_per_hour = self.event_frequency / 24.0
        return random.random() < chance_per_hour
    
    def generate_event(self, is_night=False):
        """Generate a random event"""
        if not self.should_trigger_event():
            return None
        
        self.events_this_day += 1
        
        # Determine event type
        roll = random.random()
        if roll < 0.1:  # 10% critical
            return random.choice(self.CRITICAL_EVENTS).copy()
        elif roll < (0.1 + self.anomaly_chance):
            event = random.choice(self.ANOMALOUS_EVENTS).copy()
            # Anomalous events only at night
            if not is_night:
                return None
            return event
        else:  # Routine
            return random.choice(self.ROUTINE_EVENTS).copy()
    
    def reset_day(self):
        """Reset event counter for new day"""
        self.events_this_day = 0
    
    def get_event_stats(self):
        """Get current event statistics"""
        return {
            'events_today': self.events_this_day,
            'expected_daily': self.event_frequency,
            'anomaly_chance': self.anomaly_chance
        }
