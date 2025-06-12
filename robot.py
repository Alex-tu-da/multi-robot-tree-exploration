

class Robot:
    def __init__(self, name, baum, start, ziel):
        self.name = name
        self.color = 'black'
        self.baum = baum
        self.start = start
        self.ziel = ziel

        self.role = ''

        self.current = self.start
        self.target = self.start
        self.x = 0
        self.y = 0

