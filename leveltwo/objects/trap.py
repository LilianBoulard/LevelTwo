from leveltwo.objects.generic import Object

"""
Trap : hit the player
"""

class Wall(Object):
    def __init__(self):
        name = "trap"
        effect = "hit"
        traversed = 1
        appareance = "trap"
        minInstances = 4
        maxInstances = 10
        super.__init__(name, effect, traversed, appareance, minInstances, maxInstances)