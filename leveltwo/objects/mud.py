from leveltwo.objects.generic import Object

"""
mud : slowing the player
"""

class Mud(Object):
    def __init__(self):
        name = "mud"
        effect = "slow"
        traversed = 1
        appareance = "mud"
        minInstances = 4
        maxInstances = 10
        super.__init__(name, effect, traversed, appareance, minInstances, maxInstances)