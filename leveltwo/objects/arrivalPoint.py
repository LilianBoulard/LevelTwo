from leveltwo.objects.generic import Object

"""
Arrival point : end point of a level
"""

class Wall(Object):
    def __init__(self):
        name = "finish"
        effect = "finish"
        traversed = 1
        appareance = "finish"
        minInstances = 1
        maxInstances = 1
        super().__init__(name, effect, traversed, appareance, minInstances, maxInstances)