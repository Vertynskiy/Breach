"""
Resource Manager
Manages game resources (fuel, food, water, parts, batteries)
"""

from settings import RESOURCES, DIFFICULTIES


class ResourceManager:
    """Manages all game resources"""
    
    def __init__(self, difficulty='normal'):
        """Initialize resource manager"""
        self.difficulty = difficulty
        self.difficulty_mult = DIFFICULTIES[difficulty]['resource_multiplier']
        
        # Initialize resources at their max values
        self.resources = {}
        for resource, config in RESOURCES.items():
            self.resources[resource] = config['max']
        
        # Track consumption rates
        self.consumption_rates = RESOURCES.copy()
    
    def update(self, is_night, delta_time):
        """Update resource consumption based on time of day"""
        period = 'night' if is_night else 'day'
        
        for resource_name, resource_data in self.consumption_rates.items():
            if resource_name in self.resources:
                # Get consumption rate for difficulty
                consumption = resource_data[self.difficulty][period]
                # Apply hourly consumption (delta_time is in seconds, convert to hours)
                hourly_consumption = (consumption / 3600.0) * delta_time * self.difficulty_mult
                self.resources[resource_name] += hourly_consumption
                
                # Clamp to valid range
                max_val = resource_data['max']
                self.resources[resource_name] = max(0, min(max_val, self.resources[resource_name]))
    
    def get(self, resource_name):
        """Get current amount of a resource"""
        return self.resources.get(resource_name, 0)
    
    def modify(self, resource_name, amount):
        """Add or remove a resource amount"""
        if resource_name in self.resources:
            config = RESOURCES.get(resource_name, {})
            max_val = config.get('max', 999)
            self.resources[resource_name] += amount
            self.resources[resource_name] = max(0, min(max_val, self.resources[resource_name]))
    
    def set(self, resource_name, amount):
        """Set resource to exact amount"""
        if resource_name in self.resources:
            config = RESOURCES.get(resource_name, {})
            max_val = config.get('max', 999)
            self.resources[resource_name] = max(0, min(max_val, amount))
    
    def is_critical(self, resource_name):
        """Check if resource is at critical level"""
        current = self.get(resource_name)
        config = RESOURCES.get(resource_name, {})
        critical_level = config.get('critical', 0)
        return current <= critical_level
    
    def is_depleted(self, resource_name):
        """Check if resource is completely depleted"""
        return self.get(resource_name) <= 0
    
    def has_light(self):
        """Check if there's enough fuel/batteries for light"""
        fuel = self.get('fuel')
        batteries = self.get('batteries')
        return fuel > 0 or batteries > 0
    
    def get_all(self):
        """Get all resources as dict"""
        return self.resources.copy()
    
    def get_status(self):
        """Get status of all resources"""
        status = {}
        for resource_name, amount in self.resources.items():
            config = RESOURCES.get(resource_name, {})
            max_val = config.get('max', 100)
            status[resource_name] = {
                'amount': amount,
                'max': max_val,
                'percent': (amount / max_val) * 100,
                'critical': self.is_critical(resource_name),
                'depleted': self.is_depleted(resource_name)
            }
        return status
