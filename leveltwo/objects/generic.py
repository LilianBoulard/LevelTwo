"""
Implements a generic object.
Must be inherited by all other objects.
"""

class Object:
    def __init__(self, name, effect, traversed, appearance, minInstances, maxInstances):
        self.name = name
        self.effect = effect
        self.traversed = traversed
        self.appearance = appearance
        self.minInstances = minInstances
        self.maxInstances = maxInstances