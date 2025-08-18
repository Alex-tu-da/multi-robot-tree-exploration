class Gruppe:
    def __init__(self, roboter, start, x, y):

        self.roboter = roboter
        self.role = 'Head'
        self.anzahl = len(roboter)
        self.color = 'white'
        #self.color = "rgba(0, 0, 0, 0)" #Transparent

        self.current = start
        self.target = start
        self.x = x
        self.y = y

        self.pfad = []

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color
