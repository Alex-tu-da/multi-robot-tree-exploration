class zielRobot:
    def __init__(self, start, x, y):
        self.role = 'Ziel'
        self.color = 'blue'
        self.current = start
        self.target = start
        self.x = x
        self.y = y

        self.kill_knoten = []
        self.inGefahr = False
        self.gefangen = False

    def getPosition(self):
        return [self.x, self.y]

    def zurueckFahren(self, x, y):
        self.kill_knoten.append(self.current)
        self.kill_knoten.append(self.target)

        self.target = self.current
        self.x = x[self.current]
        self.y = y[self.current]

        self.inGefahr = False