from leveltwo.objects.generic import Object

"""
Start point : beginning point of a level
"""

class Wall(Object):
    def __init__(self):
        name = "start"
        effect = "start"
        traversed = 1
        appareance = "start"
        minInstances = 1
        maxInstances = 1
        super.__init__(name, effect, traversed, appareance, minInstances, maxInstances)