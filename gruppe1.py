def vereinen(g1, g2):
    g1.roboter = g1.roboter + g2.roboter
    g1.anzahl = len(g1.roboter)
def isVereinen(g1 ,g2):
    if g1 == g2:
        return False
    elif g1.role == "Ampel" or g2.role == "Ampel":
        return False
    if g1.current == g2.current == g2.target == g1.target:
        return True
    else:
        return False

# Rolen:
# Head
# Ampel
# Schuss
class Gruppe1:
    def __init__(self, roboter, role, current, target):

        self.role = role
        self.roboter = roboter
        self.current = current
        self.target = target
        self.static = True

        self.pfad = []
        self.headKnote = -1
        if role == "Head":
            self.headKnote = target

    def getPosition(self):
        return [self.roboter[0].x, self.roboter[0].y]

    def anzahl(self):
        return len(self.roboter)

    def zurueckFahren(self):
        current = self.current
        self.current = self.target
        self.target = current
