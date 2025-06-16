
class Gruppe:
    def __init__(self, roboter, start, x, y):


        self.roboter = roboter
        self.role = 'Head'
        self.anzahl = len(roboter)
        self.color = 'white'
        #self.color = "rgba(0, 0, 0, 0)"

        self.current = start
        self.target = start
        self.x = x
        self.y = y

        self.links = -1
        self.mitte = -1
        self.rechts = -1

    def setRoleAmpel(self):
        self.role = 'Ampel'


    def getColor(self):
        return self.color