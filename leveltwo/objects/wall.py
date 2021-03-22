from leveltwo.objects.generic import Object

"""
Wall : can't be traversed
"""

class Wall(Object):
    def __init__(self):
        name = "wall"
        effect = "stop"
        traversed = 0
        appareance = "wall"
        minInstances = 4
        maxInstances = 10
        super.__init__(name, effect, traversed, appareance, minInstances, maxInstances)