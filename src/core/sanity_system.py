"""
Sanity System
Manages player sanity and mental state with difficulty scaling
"""

from settings import SANITY_RANGES, SANITY_MODIFIERS, FRACTURED_TIMEOUT, DIFFICULTIES


class SanitySystem:
    """Manages player sanity state"""
    
    def __init__(self, difficulty='normal'):
        """Initialize sanity system"""
        self.difficulty = difficulty
        self.sanity = DIFFICULTIES[difficulty]['starting_sanity']
        self.sanity_penalty_mult = DIFFICULTIES[difficulty]['sanity_penalty_mult']
        self.fractured_timer = 0
        self.state = self._get_state()
    
    def _get_state(self):
        """Determine sanity state based on current level"""
        for state_name, (min_val, max_val) in SANITY_RANGES.items():
            if min_val <= self.sanity <= max_val:
                return state_name
        return 'fractured'
    
    def update(self, delta_change):
        """Update sanity based on accumulated changes"""
        self.sanity += delta_change * self.sanity_penalty_mult
        self.sanity = max(0, min(100, self.sanity))
        
        # Update state
        new_state = self._get_state()
        
        # Check fractured timeout
        if new_state == 'fractured':
            self.fractured_timer += 1
            if self.fractured_timer >= FRACTURED_TIMEOUT:
                return True  # Game over
        else:
            self.fractured_timer = 0
        
        self.state = new_state
        return False
    
    def modify(self, amount):
        """Modify sanity by specific amount"""
        self.sanity += amount * self.sanity_penalty_mult
        self.sanity = max(0, min(100, self.sanity))
        self.state = self._get_state()
    
    def apply_event(self, event_severity):
        """Apply sanity penalty from events"""
        penalty_key = f'event_{event_severity}'
        if penalty_key in SANITY_MODIFIERS:
            self.modify(SANITY_MODIFIERS[penalty_key])
    
    def apply_environmental(self, is_dark=False, is_isolated=False):
        """Apply environmental sanity effects"""
        if is_dark:
            self.modify(SANITY_MODIFIERS['darkness'])
        if is_isolated:
            self.modify(SANITY_MODIFIERS['isolation'])
    
    def recover_from_logs(self, log_type='neutral'):
        """Recover sanity from reading director's logs"""
        if log_type in SANITY_MODIFIERS['log_finding']:
            recovery = SANITY_MODIFIERS['log_finding'][log_type]
            self.modify(recovery)
    
    def get_level(self):
        """Get current sanity level (0-100)"""
        return int(self.sanity)
    
    def get_state(self):
        """Get current sanity state"""
        return self.state
    
    def is_fractured(self):
        """Check if sanity is fractured"""
        return self.state == 'fractured'
    
    def is_panicked(self):
        """Check if sanity is in panicked state"""
        return self.state == 'panicked'
    
    def is_stable(self):
        """Check if sanity is stable"""
        return self.state == 'stable'
    
    def get_visual_effects(self):
        """Get visual effects to apply based on sanity state"""
        effects = {
            'stable': [],
            'anxious': ['audio_glitch', 'screen_flicker'],
            'panicked': ['visual_hallucination', 'false_alarm'],
            'fractured': ['severe_distortion', 'color_inversion']
        }
        return effects.get(self.state, [])
